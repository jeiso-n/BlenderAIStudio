# Pole Drift — Audio Asset License Manifest

All audio assets used in the Pole Drift soundtrack were **created originally** for this project using deterministic procedural synthesis and FFmpeg signal processing in [`build_audio.py`](file:///d:/Projects/BlenderAIStudio/projects/pole-drift/audio/build_audio.py). No external third-party, copyrighted, or unverified audio files were downloaded or used.

| Filename | Path | Creator / Artist | Source / Method | Exact License | Creation Date | Attribution Requirements |
|---|---|---|---|---|---|---|
| `engine_raw.wav` | `audio/assets/engine_raw.wav` | Blender AI Studio (Antigravity Audio Builder) | Original procedural synthesis (`gen_engine_raw` in `audio/build_audio.py`) | Original Studio Creation / CC0-equivalent (unencumbered) | 2026-11-19 | None required; credit Blender AI Studio if redistributed |
| `tires_raw.wav` | `audio/assets/tires_raw.wav` | Blender AI Studio (Antigravity Audio Builder) | Original procedural synthesis (`gen_tires_raw` in `audio/build_audio.py`) | Original Studio Creation / CC0-equivalent (unencumbered) | 2026-11-19 | None required; credit Blender AI Studio if redistributed |
| `env_raw.wav` | `audio/assets/env_raw.wav` | Blender AI Studio (Antigravity Audio Builder) | Original procedural synthesis (`gen_environment_raw` in `audio/build_audio.py`) | Original Studio Creation / CC0-equivalent (unencumbered) | 2026-11-19 | None required; credit Blender AI Studio if redistributed |
| `cinematic_raw.wav` | `audio/assets/cinematic_raw.wav` | Blender AI Studio (Antigravity Audio Builder) | Original procedural synthesis (`gen_cinematic_raw` in `audio/build_audio.py`) | Original Studio Creation / CC0-equivalent (unencumbered) | 2026-11-19 | None required; credit Blender AI Studio if redistributed |
| `music_raw.wav` | `audio/assets/music_raw.wav` | Blender AI Studio (Antigravity Audio Builder) | Original procedural composition & synthesis (`gen_music_raw` in `audio/build_audio.py`, 124 BPM D minor) | Original Studio Creation / CC0-equivalent (unencumbered) | 2026-11-19 | None required; credit Blender AI Studio if redistributed |

## Derived Stems & Mixes
- `audio/stems/01_engine.wav` — derived from `engine_raw.wav` via FFmpeg mastering chain
- `audio/stems/02_tires.wav` — derived from `tires_raw.wav` via FFmpeg mastering chain
- `audio/stems/03_environment.wav` — derived from `env_raw.wav` via FFmpeg mastering chain
- `audio/stems/04_cinematic.wav` — derived from `cinematic_raw.wav` via FFmpeg mastering chain
- `audio/stems/05_music.wav` — derived from `music_raw.wav` via FFmpeg mastering chain
- `audio/mix_preview.wav` — 5-stem stereo mix
- `pole_drift_sound_preview.mp4` — `preview.mp4` (lossless video copy) + `audio/mix_preview.wav` (AAC 192 kbps)
