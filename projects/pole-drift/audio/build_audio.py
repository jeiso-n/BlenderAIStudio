"""Reproducible audio synthesis, spatialization, and mixing pipeline for Pole Drift.

Generates 5 physics-synchronized stereo stems (48 kHz, 16-bit PCM WAV) and the
master preview mix `audio/mix_preview.wav`, then muxes with the picture-locked
`preview.mp4` into `pole_drift_sound_preview.mp4`.

Usage:
    python audio/build_audio.py
"""
import array
import math
import os
import random
import subprocess
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(HERE)
ASSETS_DIR = os.path.join(HERE, "assets")
STEMS_DIR = os.path.join(HERE, "stems")

VIDEO_IN = os.path.join(PROJECT_DIR, "preview.mp4")
MIX_OUT = os.path.join(HERE, "mix_preview.wav")
VIDEO_OUT = os.path.join(PROJECT_DIR, "pole_drift_sound_preview.mp4")

SR = 48000
DURATION = 15.0
N_SAMPLES = int(SR * DURATION)

# ------------------------------------------------------------------ car/cam geometry (mirrors build_pole_drift.py)
R = 6.2
OMEGA = math.pi / 2
V = OMEGA * R
T_IN = 3.0
PHI_START = -math.pi / 2
SWEEP = math.radians(720 + 128)
T_ARC_END = T_IN + SWEEP / OMEGA
PHI_END = PHI_START + SWEEP
DRIFT_ANGLE = math.radians(36)


def smooth(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def car_state(t: float) -> dict:
    if t < T_IN:
        x, y, phi = V * (t - T_IN), -R, PHI_START
    elif t <= T_ARC_END:
        phi = PHI_START + OMEGA * (t - T_IN)
        x, y = R * math.cos(phi), R * math.sin(phi)
    else:
        phi = PHI_END
        ex, ey = R * math.cos(phi), R * math.sin(phi)
        tx, ty = -math.sin(phi), math.cos(phi)
        x, y = ex + tx * V * (t - T_ARC_END), ey + ty * V * (t - T_ARC_END)
    drift = smooth((t - 2.2) / 1.6) * (1.0 - smooth((t - 11.8) / 1.8))
    wob = math.sin(2.0 * math.pi * t / 1.9)
    alpha = DRIFT_ANGLE * drift + math.radians(1.8) * wob * drift
    return {"x": x, "y": y, "drift": drift, "alpha": alpha, "wob": wob}


def cam_pos(t: float) -> tuple[float, float, float]:
    u = smooth(t / DURATION)
    az = math.radians(-52.0) + math.radians(22.0) * u
    return 18.0 * math.cos(az), 18.0 * math.sin(az), 8.0


def spatial_params(t: float) -> tuple[float, float, float, float]:
    """Return (dist_gain, doppler_ratio, pan [-1..1], behind_pole [0..1])."""
    dt = 0.005
    st0 = car_state(t)
    st1 = car_state(t + dt)
    cx0, cy0, cz0 = cam_pos(t)
    cx1, cy1, cz1 = cam_pos(t + dt)

    dx0, dy0, dz0 = st0["x"] - cx0, st0["y"] - cy0, 0.5 - cz0
    dx1, dy1, dz1 = st1["x"] - cx1, st1["y"] - cy1, 0.5 - cz1
    d0 = math.sqrt(dx0 * dx0 + dy0 * dy0 + dz0 * dz0)
    d1 = math.sqrt(dx1 * dx1 + dy1 * dy1 + dz1 * dz1)

    v_rad = (d1 - d0) / dt
    doppler = max(0.88, min(1.12, 343.0 / (343.0 + v_rad)))
    dist_gain = min(1.0, (14.0 / max(12.0, d0)) ** 1.15)

    cl = math.hypot(cx0, cy0)
    rx, ry = -cy0 / cl, cx0 / cl
    horiz = math.hypot(dx0, dy0) or 1.0
    pan = max(-0.92, min(0.92, (dx0 * rx + dy0 * ry) / horiz * 1.35))

    behind_pole = smooth((st0["y"] - 1.5) / 4.5)
    return dist_gain, doppler, pan, behind_pole


def pan_gains(pan: float) -> tuple[float, float]:
    """Equal-power stereo pan law for pan in [-1, 1]."""
    ang = (pan + 1.0) * 0.25 * math.pi
    return math.cos(ang), math.sin(ang)


def write_stereo_wav(path: str, left: list[float], right: list[float]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = array.array("h")
    for l_val, r_val in zip(left, right):
        il = max(-32767, min(32767, int(l_val * 32767.0)))
        ir = max(-32767, min(32767, int(r_val * 32767.0)))
        buf.append(il)
        buf.append(ir)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(buf.tobytes())


# ------------------------------------------------------------------ 1. Engine raw synthesis
def gen_engine_raw(out_path: str) -> None:
    print("Synthesizing engine_raw.wav ...")
    rng = random.Random(101)
    left = [0.0] * N_SAMPLES
    right = [0.0] * N_SAMPLES

    phase = 0.0
    turbo_phase = 0.0
    lp_state = 0.0
    inv_sr = 1.0 / SR

    for i in range(N_SAMPLES):
        t = i * inv_sr
        st = car_state(t)
        dist_gain, doppler, pan, behind = spatial_params(t)

        # RPM profile: approach climb -> turn-in surge -> sustained drift -> exit upshift/recede
        base_rpm = 3300.0 + 1600.0 * smooth(t / 2.2)
        turn_surge = 1750.0 * smooth((t - 1.9) / 0.9) * (1.0 - smooth((t - 12.2) / 1.4))
        lap1_push = 320.0 * math.exp(-((t - 7.1) ** 2) / 0.8)
        lap2_push = 280.0 * math.exp(-((t - 11.1) ** 2) / 0.7)
        exit_rpm = 800.0 * smooth((t - 12.4) / 2.0) * (1.0 - 0.5 * smooth((t - 13.5) / 1.5))
        rpm = base_rpm + turn_surge + lap1_push + lap2_push + exit_rpm + 140.0 * st["wob"] * st["drift"]

        # 6-cylinder 4-stroke: 3 firing events per revolution
        f_fire = (rpm / 60.0) * 3.0 * doppler
        phase = (phase + f_fire * inv_sr) % 1.0
        turbo_phase = (turbo_phase + f_fire * 6.5 * inv_sr) % 1.0

        # Asymmetric combustion wave + harmonics + sub-octave exhaust growl
        p2 = 2.0 * math.pi * phase
        comb = (
            0.55 * math.sin(p2)
            + 0.38 * math.sin(2.0 * p2 + 0.3)
            + 0.24 * math.sin(3.0 * p2 + 0.7)
            + 0.14 * math.sin(4.0 * p2 + 1.1)
            + 0.08 * math.sin(6.0 * p2)
            + 0.30 * math.sin(0.5 * p2)
        )
        # Soft saturation for engine grit
        drive = 1.6 + 1.2 * st["drift"]
        comb = math.tanh(comb * drive)

        # Subtle intake/turbo whistle + exhaust noise
        noise = rng.uniform(-1.0, 1.0)
        turbo = 0.04 * (0.3 + 0.7 * st["drift"]) * math.sin(2.0 * math.pi * turbo_phase)
        raw = comb * 0.78 + noise * (0.08 + 0.08 * st["drift"]) + turbo

        # Distance & behind-pole air absorption (simple 1-pole low-pass)
        cutoff_coeff = 0.38 - 0.14 * behind - 0.12 * (1.0 - dist_gain)
        lp_state += max(0.06, cutoff_coeff) * (raw - lp_state)

        # Fade in 0..0.25s and fade out 14.3..15.0s
        env = smooth(t / 0.25) * (1.0 - smooth((t - 14.3) / 0.7))
        amp = lp_state * dist_gain * env * 0.62

        gl, gr = pan_gains(pan)
        left[i] = amp * gl
        right[i] = amp * gr

    write_stereo_wav(out_path, left, right)


# ------------------------------------------------------------------ 2. Tires raw synthesis
def gen_tires_raw(out_path: str) -> None:
    print("Synthesizing tires_raw.wav ...")
    rng = random.Random(202)
    left = [0.0] * N_SAMPLES
    right = [0.0] * N_SAMPLES

    p1 = p2 = p3 = 0.0
    scrub_lp = 0.0
    mod_lp = 0.0
    inv_sr = 1.0 / SR

    for i in range(N_SAMPLES):
        t = i * inv_sr
        st = car_state(t)
        dist_gain, doppler, pan, behind = spatial_params(t)

        # Tire squeal active when drift > 0.03 (roughly 2.35s to 13.3s)
        drift = st["drift"]
        chirp = 0.25 * math.exp(-((t - 2.38) ** 2) / 0.012)
        squeal_env = min(1.0, (drift ** 0.75) * 1.05 + chirp)
        if squeal_env < 0.002:
            continue

        # Smooth random FM jitter so screech sounds organic, not robotic
        mod_lp += 0.004 * (rng.uniform(-1.0, 1.0) - mod_lp)
        slip_norm = abs(st["alpha"]) / DRIFT_ANGLE

        f_base = (1040.0 + 180.0 * slip_norm + 95.0 * st["wob"] + 160.0 * mod_lp) * doppler
        p1 = (p1 + f_base * inv_sr) % 1.0
        p2 = (p2 + f_base * 1.47 * inv_sr) % 1.0
        p3 = (p3 + f_base * 2.13 * inv_sr) % 1.0

        # Stick-slip asymmetric screech partials
        screech = (
            0.48 * math.tanh(2.2 * math.sin(2.0 * math.pi * p1))
            + 0.34 * math.sin(2.0 * math.pi * p2 + 0.4 * mod_lp)
            + 0.20 * math.sin(2.0 * math.pi * p3)
        )

        # Asphalt friction / rubber scrub noise
        n = rng.uniform(-1.0, 1.0)
        scrub_lp += 0.22 * (n - scrub_lp)
        scrub = (n - scrub_lp) * (0.35 + 0.35 * drift)

        raw = (screech * 0.55 + scrub * 0.45) * squeal_env
        att = dist_gain * (1.0 - 0.22 * behind) * 0.46
        amp = raw * att

        gl, gr = pan_gains(pan)
        left[i] = amp * gl
        right[i] = amp * gr

    write_stereo_wav(out_path, left, right)


# ------------------------------------------------------------------ 3. Environment raw synthesis
def gen_environment_raw(out_path: str) -> None:
    print("Synthesizing env_raw.wav ...")
    rng_l = random.Random(303)
    rng_r = random.Random(304)
    left = [0.0] * N_SAMPLES
    right = [0.0] * N_SAMPLES

    lp_l = lp_r = 0.0
    bp_l = bp_r = 0.0
    inv_sr = 1.0 / SR

    for i in range(N_SAMPLES):
        t = i * inv_sr
        breeze = 0.72 + 0.28 * math.sin(2.0 * math.pi * 0.17 * t + 0.4) * math.cos(2.0 * math.pi * 0.09 * t)
        env = smooth(t / 0.4) * (1.0 - smooth((t - 14.5) / 0.5))

        nl = rng_l.uniform(-1.0, 1.0)
        nr = rng_r.uniform(-1.0, 1.0)
        # Brown/pink-ish night wind
        lp_l += 0.015 * (nl - lp_l)
        lp_r += 0.015 * (nr - lp_r)
        bp_l += 0.06 * (nl * 0.25 - bp_l)
        bp_r += 0.06 * (nr * 0.25 - bp_r)

        left[i] = (lp_l * 0.8 + bp_l * 0.2) * breeze * env * 0.38
        right[i] = (lp_r * 0.8 + bp_r * 0.2) * breeze * env * 0.38

    write_stereo_wav(out_path, left, right)


# ------------------------------------------------------------------ 4. Cinematic raw synthesis
def gen_cinematic_raw(out_path: str) -> None:
    print("Synthesizing cinematic_raw.wav ...")
    rng = random.Random(404)
    left = [0.0] * N_SAMPLES
    right = [0.0] * N_SAMPLES
    inv_sr = 1.0 / SR

    sub_p = 0.0
    riser_p = 0.0
    air_lp = 0.0

    def add_whoosh(t_center: float, width: float, pan_start: float, pan_end: float, gain: float) -> None:
        i0 = max(0, int((t_center - width) * SR))
        i1 = min(N_SAMPLES, int((t_center + width) * SR))
        w_lp = 0.0
        for idx in range(i0, i1):
            t = idx * inv_sr
            u = (t - (t_center - width)) / (2.0 * width)
            env = math.sin(math.pi * u) ** 2
            w_lp += (0.04 + 0.18 * env) * (rng.uniform(-1.0, 1.0) - w_lp)
            p = pan_start + (pan_end - pan_start) * u
            gl, gr = pan_gains(p)
            val = w_lp * env * gain
            left[idx] += val * gl
            right[idx] += val * gr

    for i in range(N_SAMPLES):
        t = i * inv_sr
        # 1) Entrance sub-bass swell (0.0 - 1.3 s)
        if t < 1.35:
            e = smooth(t / 0.45) * (1.0 - smooth((t - 0.75) / 0.6))
            sub_p = (sub_p + 55.0 * inv_sr) % 1.0
            v = math.sin(2.0 * math.pi * sub_p) * e * 0.22
            left[i] += v
            right[i] += v

        # 2) Turn-in riser & impact (1.9 - 3.05 s)
        if 1.85 <= t <= 3.10:
            u = (t - 1.85) / 1.25
            f_r = 90.0 + 380.0 * (u * u)
            riser_p = (riser_p + f_r * inv_sr) % 1.0
            e = math.sin(math.pi * u) * 0.14
            v = math.sin(2.0 * math.pi * riser_p) * e
            left[i] += v * 0.85
            right[i] += v * 0.55

        # 3) Turn-in impact thump at 2.50 s
        if 2.48 <= t <= 3.05:
            dt = t - 2.48
            f_hit = 110.0 * math.exp(-dt * 9.0) + 42.0
            e = math.exp(-dt * 7.5)
            v = math.sin(2.0 * math.pi * f_hit * dt) * e * 0.30
            left[i] += v * 0.8
            right[i] += v * 0.6

        # 4) Strongest drift moment accent at 7.25 s (Lap 1 peak)
        if 7.15 <= t <= 8.00:
            dt = t - 7.15
            f_hit = 125.0 * math.exp(-dt * 8.0) + 45.0
            e = math.exp(-dt * 5.5)
            v = math.sin(2.0 * math.pi * f_hit * dt) * e * 0.34
            left[i] += v
            right[i] += v

        # 5) Controlled exit downward sweep (12.35 - 13.70 s)
        if 12.35 <= t <= 13.75:
            u = max(0.0, min(1.0, (t - 12.35) / 1.40))
            f_d = 260.0 * ((1.0 - u) ** 1.6) + 55.0
            riser_p = (riser_p + f_d * inv_sr) % 1.0
            e = math.sin(math.pi * u) * 0.16
            air_lp += 0.05 * (rng.uniform(-1.0, 1.0) - air_lp)
            v = (math.sin(2.0 * math.pi * riser_p) * 0.6 + air_lp * 0.4) * e
            left[i] += v * 0.5
            right[i] += v * 0.9

    add_whoosh(3.55, 0.45, -0.45, 0.45, 0.24)
    add_whoosh(7.30, 0.55, -0.40, 0.45, 0.32)
    add_whoosh(11.35, 0.45, -0.45, 0.45, 0.25)

    write_stereo_wav(out_path, left, right)


# ------------------------------------------------------------------ 5. Music raw synthesis (124 BPM dark synthwave)
def midi_to_hz(m: int) -> float:
    return 440.0 * (2.0 ** ((m - 69) / 12.0))


def gen_music_raw(out_path: str) -> None:
    print("Synthesizing music_raw.wav ...")
    rng = random.Random(505)
    left = [0.0] * N_SAMPLES
    right = [0.0] * N_SAMPLES

    bpm = 124.0
    beat_dur = 60.0 / bpm          # 0.48387 s
    step_dur = beat_dur / 4.0      # 16th note = 0.12097 s
    inv_sr = 1.0 / SR

    # D minor progression (4 bars = 16 beats = 7.74s -> ~2 phrases in 15s)
    # Bar 1: Dm (D2=38), Bar 2: Bb (Bb1=34), Bar 3: Gm (G1=31), Bar 4: A (A1=33)
    bass_roots = [38, 34, 31, 33]
    pad_chords = [
        [50, 57, 62, 65],  # Dm
        [46, 53, 58, 62],  # Bb
        [43, 50, 55, 58],  # Gm
        [45, 52, 57, 61],  # A
    ]
    arp_patterns = [
        [62, 65, 69, 74],  # Dm
        [58, 62, 65, 70],  # Bb
        [55, 58, 62, 67],  # Gm
        [57, 61, 64, 69],  # A
    ]

    bass_p = 0.0
    arp_p1 = arp_p2 = 0.0
    pad_ps = [0.0, 0.0, 0.0, 0.0]
    bass_lp = arp_lp = snare_lp = hat_lp = 0.0

    for i in range(N_SAMPLES):
        t = i * inv_sr
        beat_f = t / beat_dur
        beat_idx = int(beat_f)
        beat_pos = beat_f - beat_idx
        bar_idx = (beat_idx // 4) % 4
        step_f = t / step_dur
        step_idx = int(step_f)
        step_pos = step_f - step_idx

        # Energy arc: 0..1.9s intro -> 1.9..3.0s build -> 3.0..12.1s full -> 12.1..15.0s resolve
        if t < 1.9:
            drum_lvl = 0.25 * smooth(t / 1.5)
            arp_lvl = 0.18 + 0.25 * smooth(t / 1.9)
        elif t < 3.0:
            drum_lvl = 0.35 + 0.65 * smooth((t - 1.9) / 1.1)
            arp_lvl = 0.43 + 0.45 * smooth((t - 1.9) / 1.1)
        elif t < 12.1:
            drum_lvl = 1.0
            arp_lvl = 0.90 + 0.10 * smooth((t - 5.5) / 2.0)
        else:
            drum_lvl = max(0.0, 1.0 - smooth((t - 12.1) / 0.5))
            arp_lvl = max(0.0, 0.85 * (1.0 - smooth((t - 12.3) / 1.6)))

        master_env = smooth(t / 0.3) * (1.0 - smooth((t - 14.15) / 0.85))

        # --- Kick (every beat) ---
        kick = 0.0
        if drum_lvl > 0.05 and t < 12.35:
            kt = beat_pos * beat_dur
            if kt < 0.22:
                kf = 135.0 * math.exp(-kt * 28.0) + 46.0
                ke = math.exp(-kt * 14.0)
                kick = math.sin(2.0 * math.pi * kf * kt) * ke * 0.58 * drum_lvl

        # --- Snare (beats 2 & 4, i.e. beat_idx % 2 == 1, active from 1.9s) ---
        snare = 0.0
        if t >= 1.90 and t < 12.35 and (beat_idx % 2 == 1):
            st_t = beat_pos * beat_dur
            if st_t < 0.18:
                body = math.sin(2.0 * math.pi * 195.0 * st_t) * math.exp(-st_t * 24.0)
                n = rng.uniform(-1.0, 1.0)
                snare_lp += 0.35 * (n - snare_lp)
                snare = (body * 0.45 + (n - snare_lp) * 0.55) * math.exp(-st_t * 18.0) * 0.42 * drum_lvl

        # --- Hi-hat (8th/16th offbeats) ---
        hat = 0.0
        if t >= 3.00 and t < 12.20 and (step_idx % 2 == 1):
            ht = step_pos * step_dur
            if ht < 0.055:
                n = rng.uniform(-1.0, 1.0)
                hat_lp += 0.55 * (n - hat_lp)
                hat = (n - hat_lp) * math.exp(-ht * 65.0) * 0.16 * drum_lvl

        # --- Rolling 16th-note Synth Bass ---
        f_bass = midi_to_hz(bass_roots[bar_idx])
        bass_p = (bass_p + f_bass * inv_sr) % 1.0
        saw_b = 2.0 * bass_p - 1.0
        sub_b = math.sin(2.0 * math.pi * bass_p)
        b_env = math.exp(-step_pos * 2.2) * (0.35 + 0.65 * smooth(t / 2.8))
        if t > 12.3:
            b_env *= max(0.0, 1.0 - smooth((t - 12.3) / 1.5))
        bass_lp += (0.06 + 0.18 * b_env) * ((saw_b * 0.6 + sub_b * 0.4) - bass_lp)
        bass = bass_lp * b_env * 0.40

        # --- Wide Detuned Pad ---
        chord = pad_chords[0] if t >= 12.35 else pad_chords[bar_idx]
        pad_l = pad_r = 0.0
        for idx, note in enumerate(chord):
            fn = midi_to_hz(note)
            pad_ps[idx] = (pad_ps[idx] + fn * inv_sr) % 1.0
            w = math.sin(2.0 * math.pi * pad_ps[idx]) + 0.35 * math.sin(4.0 * math.pi * pad_ps[idx])
            if idx % 2 == 0:
                pad_l += w
                pad_r += w * 0.7
            else:
                pad_l += w * 0.7
                pad_r += w
        pad_amp = 0.065 * (0.5 + 0.5 * smooth(t / 3.0))

        # --- Driving 16th-note Arp Lead ---
        arp_note = arp_patterns[bar_idx][step_idx % 4]
        f_arp = midi_to_hz(arp_note)
        arp_p1 = (arp_p1 + f_arp * inv_sr) % 1.0
        arp_p2 = (arp_p2 + f_arp * 1.004 * inv_sr) % 1.0
        arp_raw = ((2.0 * arp_p1 - 1.0) + (2.0 * arp_p2 - 1.0)) * 0.5
        a_env = math.exp(-step_pos * 3.5)
        arp_lp += (0.08 + 0.25 * a_env * arp_lvl) * (arp_raw - arp_lp)
        arp = arp_lp * a_env * arp_lvl * 0.24
        arp_pan = 0.30 * math.sin(t * 2.5)
        al, ar = pan_gains(arp_pan)

        mono_center = kick + snare + hat + bass
        left[i] = (mono_center + pad_l * pad_amp + arp * al) * master_env
        right[i] = (mono_center + pad_r * pad_amp + arp * ar) * master_env

    write_stereo_wav(out_path, left, right)


# ------------------------------------------------------------------ FFmpeg stem mastering & mixing
def run_ffmpeg(args: list[str]) -> None:
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + args
    subprocess.run(cmd, check=True)


def process_stems_and_mix() -> None:
    os.makedirs(STEMS_DIR, exist_ok=True)
    raw_eng = os.path.join(ASSETS_DIR, "engine_raw.wav")
    raw_tir = os.path.join(ASSETS_DIR, "tires_raw.wav")
    raw_env = os.path.join(ASSETS_DIR, "env_raw.wav")
    raw_cin = os.path.join(ASSETS_DIR, "cinematic_raw.wav")
    raw_mus = os.path.join(ASSETS_DIR, "music_raw.wav")

    s_eng = os.path.join(STEMS_DIR, "01_engine.wav")
    s_tir = os.path.join(STEMS_DIR, "02_tires.wav")
    s_env = os.path.join(STEMS_DIR, "03_environment.wav")
    s_cin = os.path.join(STEMS_DIR, "04_cinematic.wav")
    s_mus = os.path.join(STEMS_DIR, "05_music.wav")

    print("Mastering stems via FFmpeg ...")
    # 01_engine: warm low-mid boost, subtle air/night reverb, controlled dynamics
    run_ffmpeg([
        "-i", raw_eng,
        "-af", "highpass=f=45,equalizer=f=140:t=q:w=1.2:g=3,equalizer=f=900:t=q:w=1.0:g=2,aecho=0.8:0.75:45|75:0.18|0.12,acompressor=threshold=-16dB:ratio=2.5:attack=10:release=120,volume=0.95",
        "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", s_eng,
    ])
    # 02_tires: tame harsh 3.5k+ whistle, emphasize 1.1-2.2k rubber bite, subtle night space
    run_ffmpeg([
        "-i", raw_tir,
        "-af", "highpass=f=450,lowpass=f=4800,equalizer=f=1450:t=q:w=1.2:g=2.5,equalizer=f=3200:t=q:w=1.5:g=-3,aecho=0.8:0.75:55:0.16,acompressor=threshold=-18dB:ratio=2.8:attack=8:release=100,volume=1.35",
        "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", s_tir,
    ])
    # 03_environment: gentle night ambience bed
    run_ffmpeg([
        "-i", raw_env,
        "-af", "highpass=f=60,lowpass=f=1800,volume=1.15",
        "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", s_env,
    ])
    # 04_cinematic: wide night tail + peak control
    run_ffmpeg([
        "-i", raw_cin,
        "-af", "highpass=f=32,aecho=0.8:0.85:90|160:0.25|0.18,volume=0.88",
        "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", s_cin,
    ])
    # 05_music: polished stereo synthwave bed, restrained so engine/tires lead
    run_ffmpeg([
        "-i", raw_mus,
        "-af", "highpass=f=35,equalizer=f=2200:t=q:w=1.0:g=-1.5,aecho=0.8:0.8:60|110:0.18|0.12,acompressor=threshold=-14dB:ratio=2.2:attack=12:release=140,volume=0.72",
        "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", s_mus,
    ])

    print("Mixing stems -> audio/mix_preview.wav ...")
    # Combine engine+tires as sidechain key to gently duck music during peak drift
    filter_complex = (
        "[0:a][1:a]amix=inputs=2:duration=first:normalize=0[veh];"
        "[veh]asplit=2[veh_mix][veh_key];"
        "[4:a][veh_key]sidechaincompress=threshold=0.08:ratio=2.8:attack=25:release=220[mus_ducked];"
        "[veh_mix][2:a][3:a][mus_ducked]amix=inputs=4:duration=first:normalize=0,"
        "alimiter=limit=0.89:attack=5:release=60,afade=t=out:st=14.75:d=0.25[out]"
    )
    run_ffmpeg([
        "-i", s_eng,
        "-i", s_tir,
        "-i", s_env,
        "-i", s_cin,
        "-i", s_mus,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le",
        MIX_OUT,
    ])

    print("Muxing audio + picture-locked preview.mp4 -> pole_drift_sound_preview.mp4 ...")
    run_ffmpeg([
        "-i", VIDEO_IN,
        "-i", MIX_OUT,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2",
        "-shortest",
        VIDEO_OUT,
    ])


def main() -> None:
    os.makedirs(ASSETS_DIR, exist_ok=True)
    gen_engine_raw(os.path.join(ASSETS_DIR, "engine_raw.wav"))
    gen_tires_raw(os.path.join(ASSETS_DIR, "tires_raw.wav"))
    gen_environment_raw(os.path.join(ASSETS_DIR, "env_raw.wav"))
    gen_cinematic_raw(os.path.join(ASSETS_DIR, "cinematic_raw.wav"))
    gen_music_raw(os.path.join(ASSETS_DIR, "music_raw.wav"))
    process_stems_and_mix()
    print("Done! Created:", MIX_OUT, "and", VIDEO_OUT)


if __name__ == "__main__":
    main()
