# Pole Drift — Audio Production Plan & Frame-Accurate Cue Sheet

**Project:** Pole Drift (`projects/pole-drift/`)  
**Picture Lock Master:** `preview.mp4` (`640x360`, `24 fps`, `360 frames`, `15.000 s`, H.264 High, silent)  
**Editable Source:** `pole_drift.blend` (and deterministic generator `build_pole_drift.py`)  
**Sound Identity:** Hybrid automotive soundscape — realistic synthesized/spatialized vehicle & tire layers + subtle nighttime outdoor ambience + restrained cinematic accents + modern dark-synthwave/electronic instrumental (no vocals).  
**Audio Format Target:** 48 kHz, 16-bit PCM stereo stems (`audio/stems/*.wav`) and master preview mix (`audio/mix_preview.wav`); AAC-LC 192 kbps stereo muxed into `pole_drift_sound_preview.mp4`.

---

## 1. Spatialization & Physics Mapping

All diegetic vehicle audio (`01_engine.wav` and `02_tires.wav`) is driven directly by the exact closed-form `car_state(t)` and `cam_pos(t)` geometry from `build_pole_drift.py`:
- **Distance Attenuation:** Inverse-distance scaling `g_dist(t) = clamp(14.0 / dist(t), 0.25, 1.0)` with distance-dependent high-frequency air absorption (subtle low-pass darkening as `dist` grows from 14 m to 42 m or when passing behind the pole).
- **Doppler Shift:** Pitch ratio `343.0 / (343.0 + v_rad(t))` computed from radial velocity `d(dist)/dt`, giving authentic pitch rise on approach/foreground sweep and pitch drop on recede/exit.
- **Stereo Pan:** Equal-power pan law derived from the horizontal dot product of `(car - cam)` with the camera right vector (`-0.88` far left on entry, sweeping `-0.45 -> +0.46` across foreground passes, narrowing `+0.30 -> -0.26` behind the pole, settling at `+0.49` upper-right on exit).

---

## 2. Frame-Accurate Cue Sheet (24 fps, Frames 1–360, 0.000–15.000 s)

| Frame | Time (s) | Visual Action | Engine (`01_engine`) | Tires (`02_tires`) | Environment (`03_environment`) | Cinematic (`04_cinematic`) | Music (`05_music`) | Stereo Pan |
|---|---|---|---|---|---|---|---|---|
| **1–24** | 0.00–1.00 | Empty night drift pad under pole spotlight; car approaches off-screen left (`dist` 41.8→32.5 m). | Distant low-mid V6/inline-6 rumble & intake purr; RPM ~3200→3800, rising gently as car nears frame. | Silent (`drift = 0.0`). | Steady subtle night wind & open-pad air (-32 LUFS). | Restrained sub-bass atmospheric swell (0.00–1.20 s) establishing night tension. | Filtered dark-synthwave pad + muted pulse kick/arp intro (124 BPM, D minor), low-pass opening. | `-0.88` → `-0.82` |
| **25–46** | 1.00–1.92 | Car nose & headlights enter frame-left (`f25`), full car enters (`f49`); straight approach (`dist` 32.5→24.4 m). | Throttle opens; RPM climbs 3800→4900, exhaust bark sharpens, subtle turbo spool. | Silent (`drift = 0.0`). | Night wind steady. | Subtle approach air whoosh building toward turn-in. | Kick/snare groove locks in at `1.94 s` (bar 2); bassline enters low. | `-0.82` → `-0.70` |
| **47–72** | 1.92–3.00 | Turn-in steer flick (`f47`), yaw ramps in (`f54`), **skid marks begin (`f61`, 2.50 s)**; car enters spotlight pool (`dist` 24.4→15.8 m). | Hard downshift/throttle blip & RPM surge 4900→6400; high-load growl as rear breaks traction. | Initial tire chirp at `2.35 s`, ramping into sharp dual-formant squeal + asphalt scrub at `2.50 s` (`f61`). | Wind steady, slightly ducked under car. | **Turn-in impact accent** (`2.50 s`) + riser into main drift drop. | Synth riser & filter sweep peaking at `3.00 s` (bar 3 downbeat). | `-0.70` → `-0.39` |
| **73–108** | 3.00–4.50 | **Circular drift begins (`f73`, 3.00 s)**, **smoke puffs start (`f73`)**; car sweeps foreground left-to-right (`dist` 14.0 m min at `3.50 s`). | Full drift load (RPM 6200–6900 with 1.9 s wobble modulation), rich exhaust & intake roar at peak proximity. | Full sustained tire squeal (`drift` 0.50→1.00) with pitch modulation from slip wobble (34–38°). | Subtle ambience underneath. | **Foreground pass whoosh #1** (`3.30–3.80 s`) reinforcing close sweep. | **Main beat drop (`3.00 s`)**: full punchy kick, driving 16th-note synth bass, crisp hats, arpeggiated lead. | `-0.39` → `+0.43` |
| **109–156** | 4.50–6.50 | Car sweeps behind the pole (`f121`, 5.00 s, `dist` 24.1 m) and around the far-left arc (`f145`, 6.00 s). | Sustained load, level attenuates ~4 dB and high-end softens slightly behind pole; Doppler drop then rise. | Continuous tire squeal, slightly softer & warmer behind pole, subtle pitch dip/rise. | Steady night air. | Clean (no extra hit; let diegetic spatialization breathe). | Driving groove continues; subtle high-arp octave layer enters at `5.80 s`. | `+0.43` → `-0.26` |
| **157–196** | 6.50–8.17 | **Lap 1 peak closest foreground pass** (`f175`, 7.25 s, `dist` 14.8 m); heavy smoke trail & headlights sweep across camera. | Peak proximity roar, slight RPM surge (6500→7100) + brief throttle feather/pop around `7.5 s`. | Peak intensity tire screech + gritty asphalt friction at closest pass. | Steady night air. | **Strongest drift moment accent (`7.25 s`)**: tight sub-thump + wide stereo air-rush. | Music energy peak (full synth lead + bass + percussion, ducked -2.5 dB under peak tires/engine). | `-0.29` → `+0.39` |
| **197–252** | 8.17–10.50 | Lap 2 far side behind pole (`f217`, 9.00 s, `dist` 23.6 m) and far-left curve (`f241`, 10.00 s). | Sustained high-RPM drift load, distance-attenuated behind pole, building back as car rounds left. | Sustained skid, realistic intensity & pitch modulation matching `alpha(t)`. | Steady night air. | Clean. | Driving synthwave groove sustained; subtle tension build toward final lap exit. | `+0.30` → `-0.21` |
| **253–298** | 10.50–12.42 | **Lap 2 foreground pass** (`f265`, 11.00 s) & **slip ramp-down begins (`f284`, 11.79 s)**; car finishes 128° exit arc (`f299`, 12.42 s). | High-load roar through foreground (`11.0–11.8 s`), then slight lift/upshift as car straightens out (`11.8–12.4 s`). | Strong foreground squeal (`11.0–11.8 s`), then squeal tapers off smoothly (`11.8–12.8 s`) into scrub. | Steady night air. | **Foreground pass whoosh #2** (`11.40 s`). | Final bar climax (`11.61 s`), percussion drops to half-time/filtered out at `12.50 s`. | `-0.45` → `+0.46` |
| **299–322** | 12.42–13.38 | **Straight exit** onto upper-right tangent; **smoke stops (`f308`, 12.79 s)**, **skid marks end (`f322`, 13.38 s)**. | Smooth acceleration away (`dist` 18.4→27.1 m), Doppler pitch drop, exhaust note receding. | Tire squeal fades completely by `12.85 s`; faint tire-on-asphalt roll noise until `13.38 s`. | Night wind becomes more audible as car recedes. | **Controlled exit transition** (`12.40–13.40 s`): soft downward synth/air sweep. | Drums out; warm sustained D-minor synth chord + decaying arpeggio tail. | `+0.46` → `+0.47` |
| **323–360** | 13.38–15.00 | Car recedes straight into upper-right night distance (`dist` 27.1→42.1 m), tail lights small at `f360`. | Distant receding exhaust hum fading cleanly into night ambience by `14.85 s`. | Silent (`drift = 0.0`). | Night wind ambience holds cleanly, gentle fade-out `14.60–15.00 s` to avoid abrupt cut. | Subtle reverb tail only. | Sustained final D-minor chord resolves and fades out naturally `14.20–15.00 s`. | `+0.48` → `+0.49` |

---

## 3. Mixing & Loudness Targets

- **Engine (`01_engine`):** Primary anchor; sits clearly in front during approach and foreground passes.
- **Tires (`02_tires`):** Co-lead with engine during `2.50–12.80 s` drift; sculpted around 1.0–2.8 kHz so it cuts through without harsh ear fatigue.
- **Environment (`03_environment`):** Subtle bed (-30 to -34 LUFS), never masking engine or tires.
- **Cinematic (`04_cinematic`):** Punctuation only at `0.0–1.2 s`, `2.50 s`, `3.50 s`, `7.25 s`, `11.40 s`, `12.50 s`.
- **Music (`05_music`):** Supportive modern dark-synthwave bed (-18 to -20 LUFS), dynamically ducked during peak drift (`3.0–12.0 s`) so engine + tires remain unmistakable.
- **Master (`mix_preview.wav`):** 48 kHz / 16-bit stereo, integrated loudness ~`-14.5` to `-16.5` LUFS, true peak ≤ `-1.0 dBFS` (zero clipping).
