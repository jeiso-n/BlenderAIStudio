# Pole Drift — Production Notes (low-resolution preview)

Real Blender 5.3 3D animation (Eevee). No AI video generation, no external services.

## Files
| File | Purpose |
|---|---|
| `build_pole_drift.py` | Rerunnable, deterministic build script. `blender -b --factory-startup --python build_pole_drift.py` rebuilds `pole_drift.blend` from scratch. |
| `render_pole_drift.py` | Headless render helper (`-- video` or `-- stills OUTDIR frames...`). |
| `verify_pole_drift.py` | Headless verification of the saved .blend (settings, keyframes, motion sanity checks). |
| `pole_drift.blend` | Editable scene. |
| `preview.png` | Representative still (frame 110, 640×360). |
| `preview.mp4` | 360-frame H.264 preview. |

## Scene structure (collections)
- **Environment** — `Ground` (160 m plane, asphalt), `DriftPad` (r=16 m lighter disc), `Markings_Dashed` (white dashed ring r≈11.5 m), `Markings_PoleRing` (yellow ring at pole base), `Pole` + `Pole_Bands` + `Pole_LampPanel` (6.5 m pole, emissive lamp), `Pole_LightBeam` (faint transparent cone), `Bollards` (24 emissive cyan posts, r=15.5 m — meshes, not lights), `TreeLine` (30 dark cone silhouettes).
- **Car** — `Car_Root` (path position + yaw) → `Car_Chassis` (roll/pitch/bounce, pivot on the ground) → `Car_Body` (one low-poly mesh: tapered lofted body, glassed cabin with body-colour roof, spoiler, splitter, emissive head/tail lights; Bevel modifier). Four wheels under `Car_Root` (`WheelPivot_*` steering → `WheelSpin_*` rolling → tire/hub/marker mesh). `Headlight_Spot` is parented to the car.
- **FX** — `SkidMark_RL/RR` (ribbons generated from the exact rear-wheel contact paths, revealed over time with a **Build modifier**), 118 `Puff_###` objects sharing one 20-triangle icosahedron mesh (stylised tire smoke; scale/position keyframed, no simulation).
- **Lighting_Camera** — `PoleLight` (warm point, shadows on), `Rim_Cyan` and `Fill_Blue` (area, no shadows), `Headlight_Spot` (no shadows) = 4 lights; `Camera` (28 mm) on `CamRig`, `CamTarget`, `LightTarget`.

## Animation design (24 fps, frames 1–360, 15 s)
All motion comes from the closed-form function `car_state(t)` in the build script (also used to place skid marks and smoke), sampled once per frame as keyframes (linear interpolation).

| Time | Frames | Action |
|---|---|---|
| 0–3 s | 1–73 | Car enters from off-screen left along the tangent line y=−6.2 m at constant 9.74 m/s; drift initiation (turn-in steer flick, yaw ramps in from 2.2 s). |
| 3–11 s | 73–265 | Circular drift, radius 6.2 m, 90°/s → two full laps by 11 s. Car centre truly translates on the circle. |
| 11–12.4 s | 265–~298 | Arc completes (another 128°) so the tangent points away from camera; slip angle ramps down from 11.8 s. |
| 12.4–15 s | ~298–360 | Straight exit along the tangent, receding into the distance. |

- Drift: body yaw = path heading + slip angle (≈36–40°, nose toward the pole, tail outward), small deterministic wobble.
- Steering: front wheels counter-steer (≈ −0.85× slip angle ≈ −32°) once sliding; brief steer into the turn during turn-in.
- Wheels: roll forward (rear wheels spin 10% faster, power-slide). Each wheel has an asymmetric marker so spin direction is visible at 24 fps.
- Suspension: ≤3.2° outward body roll, ≤0.8° pitch, ≤1.2 cm bounce, all scaled by drift amount; wheels never leave z=0.
- Camera: 28 mm, three-quarter high angle (18 m, 8 m high), eased 22° orbit over the shot, no cuts.

## Render settings (preview)
Eevee (`BLENDER_EEVEE`), 640×360, 24 fps, 8 samples, shadow ray count 1, no raytracing, no motion blur, AgX Medium-High-Contrast. Output: FFmpeg MPEG-4 / H.264, medium quality. Proposed final (needs approval): 1280×720, 16 samples.

## Budget
5,364 triangles in the evaluated scene at frame 360 (limit 20,000). 4 lights. 153 objects. Only primitive-built meshes, no image textures.

## Known limitations
- Low-poly stylised look: faceted smoke puffs, no tire deformation, no interior, no wheel arches (wheels partly embedded in the body sides).
- Car is a single mesh for body/cabin/lights (materials separated by slot), so it is not individually rigged beyond wheels and chassis.
- The car recedes into the distance on exit and is still a small figure in frame at frame 360 (it does not leave the frame).
- Pole light beam cone is a cheap transparent mesh, not volumetrics.
- `Material.use_nodes` / `World.use_nodes` emit Blender 6.0 deprecation warnings (harmless in 5.3).

## Audio Production (draft preview — 2026-11-19)
- **Picture lock:** `preview.mp4` (640×360, 24 fps, 360 frames, 15.000 s, silent) preserved untouched; `pole_drift.blend` untouched.
- **Reproducible pipeline:** `audio/build_audio.py` synthesizes 5 physics-synchronized 48 kHz / 16-bit stereo raw assets (`audio/assets/*.wav`) driven by `car_state(t)` and `cam_pos(t)`, masters 5 stems via FFmpeg (`audio/stems/01_engine.wav` .. `05_music.wav`), sidechain-ducks music under vehicle SFX into `audio/mix_preview.wav` (-15.2 LUFS, -2.9 dBFS true peak), and muxes with `preview.mp4` (`-c:v copy`, AAC 192 kbps) into `pole_drift_sound_preview.mp4`.
- **Documentation & QC:** `pole_drift_audio_plan.md` (frame-accurate cue sheet), `audio/licenses.md` (100% original studio synthesis), `audio_qc.md` (FFprobe + EBU R128 + sync verification), and `pole_drift_audio_workflow_viz.mp4` (synchronized waveform/spectrum diagnostic).
- **Status:** Draft audio preview complete; awaiting ChatGPT independent review before final mastering.
