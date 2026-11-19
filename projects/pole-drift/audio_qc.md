# Pole Drift — Audio Quality Control Report

**Date:** 2026-11-19  
**Reviewed Deliverable:** `pole_drift_sound_preview.mp4` + `audio/mix_preview.wav` + 5 stems (`audio/stems/*.wav`)  
**Picture-Lock Master:** `preview.mp4` (640×360, 24 fps, 360 frames, 15.000000 s, H.264 High, silent — preserved untouched)

---

## 1. Stream & Format Verification (`ffprobe`)

| Check | Expected | Observed (`pole_drift_sound_preview.mp4`) | Status |
|---|---|---|---|
| Video codec & profile | H.264 High (copied losslessly from `preview.mp4`) | `h264 (High)`, `yuv420p` | **PASS** |
| Resolution | `640x360` | `640x360` (`16:9`) | **PASS** |
| Frame rate & count | `24/1 fps`, `360` frames | `24/1 fps`, `360` frames | **PASS** |
| Container duration | `15.000000 s` | `15.000000 s` | **PASS** |
| Audio codec | AAC-LC stereo | `aac (LC)`, `fltp`, `193,195 bps` | **PASS** |
| Sample rate & channels | `48000 Hz`, `2` (`stereo`) | `48000 Hz`, `2` (`stereo`) | **PASS** |
| Audio stream duration | ~`15.000 s` | `14.997333 s` (`704` AAC frames, `-shortest` aligned) | **PASS** |

---

## 2. Loudness, True Peak & Clipping (`ffmpeg ebur128` + `volumedetect`)

| File | Integrated Loudness (LUFS) | True Peak (dBFS) | Max Sample (dB) | Mean Volume (dB) | Clipping |
|---|---|---|---|---|---|
| `audio/stems/01_engine.wav` | `-18.4 LUFS` | `-9.4 dBFS` | `-9.4 dB` | `-21.1 dB` | None |
| `audio/stems/02_tires.wav` | `-20.6 LUFS` | `-12.0 dBFS` | `-12.1 dB` | `-26.3 dB` | None |
| `audio/stems/03_environment.wav` | `-36.9 LUFS` | `-23.5 dBFS` | `-23.5 dB` | `-38.8 dB` | None |
| `audio/stems/04_cinematic.wav` | `-25.6 LUFS` | `-11.8 dBFS` | `-11.8 dB` | `-30.0 dB` | None |
| `audio/stems/05_music.wav` | `-24.2 LUFS` | `-7.9 dBFS` | `-8.2 dB` | `-25.9 dB` | None |
| **`audio/mix_preview.wav`** | **`-15.2 LUFS`** | **`-2.9 dBFS`** | **`-2.9 dB`** | **`-18.0 dB`** | **None (2.9 dB headroom)** |

---

## 3. Synchronization & Editorial Checklist

- **Audio/video duration match:** PASS (`15.000000 s` container; `0.25 s` fade-in/out prevents clicks or abrupt cuts).
- **Engine & tires vs. visible movement:** PASS — both `01_engine.wav` and `02_tires.wav` are computed directly from the closed-form `car_state(t)` and `cam_pos(t)` functions in `build_pole_drift.py`:
  - Approach (`0.00–1.92 s`): engine rises from far-left (`pan = -0.88 -> -0.70`), tires silent.
  - Turn-in & skid onset (`2.20–3.00 s`): tire chirp at `2.38 s`, full dual-formant squeal + asphalt scrub ramping at `2.50 s` (`f61`), matching `SkidMark_RL/RR` Build modifier start.
  - Circular drift (`3.00–12.42 s`): sustained engine load & tire squeal with 1.9 s slip-angle wobble, Doppler pitch shift, and distance attenuation behind the pole (`~5.0 s`, `~9.0 s`).
  - Exit (`12.42–15.00 s`): tire squeal tapers off as slip ramps down (`11.8–12.8 s`), engine recedes into upper-right (`pan = +0.49`) with Doppler drop.
- **Music balance:** PASS — `05_music.wav` (`-24.2 LUFS`) is sidechain-compressed against combined engine + tires (`01_engine + 02_tires`) so vehicle sound effects always lead.
- **Stereo imaging:** PASS — verified visually in `mix_qc_visual.png` (L/R split waveform) and `pole_drift_audio_workflow_viz.mp4`.
- **Licenses:** PASS — 100% original procedural synthesis & FFmpeg processing; documented in `audio/licenses.md`.

---

## 4. Known Issues / Limitations

1. **Procedural synthesis vs. recorded foley:** Engine and tire stems are synthesized mathematically rather than recorded from a physical car; while 100% physics-synced and license-clean, final mastering could optionally layer verified CC0 real-car/tire samples if desired by the Creative Director.
2. **Headless shell screen recording limitation:** `ffmpeg -f gdigrab` failed with Windows error `5` (Access Denied) in the non-interactive agent shell, so a live desktop capture could not be recorded from this session. A synchronized audiovisual diagnostic video (`pole_drift_audio_workflow_viz.mp4`, side-by-side `pole_drift_sound_preview.mp4` + live stereo waveform & spectrogram) was rendered instead.
3. **Human listening check pending:** Automated loudness, peak, spectrum, and sync checks all pass; final subjective listening approval awaits ChatGPT / Creative Director review.
