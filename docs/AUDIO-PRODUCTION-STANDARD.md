# Blender AI Studio — Audio Production Standard

**Version:** 1.0  
**Established:** 2026-11-19  
**Default direction:** Hybrid sound design + background music  
**Applies to:** Every animation, unless the Creative Director explicitly approves an exception.

## 1. Studio principle

An animation is an audiovisual production. Sound must be designed against the final approved picture and synchronized to visible action. Audio is a separate post-production stage: never damage, overwrite, or silently alter the approved visual master while creating the soundtrack.

The Creative Director approves the creative direction. ChatGPT is Audio Director, production planner, independent reviewer and quality gate. Antigravity is the builder/editor and production operator. Blender remains the visual production engine; FFmpeg is the preferred final muxing/encoding tool when suitable.

## 2. Default sound identity: hybrid

Every project should combine, as appropriate:
- **Diegetic / realistic sound:** sounds that plausibly exist in the scene (engines, tires, footsteps, impacts, room tone, wind, machinery, object handling).
- **Cinematic sound design:** restrained whooshes, transitions, impacts, risers, tonal accents and designed atmosphere that strengthen storytelling without drawing attention to themselves.
- **Background music:** yes by default. Music should support pacing and emotion, remain subordinate to important effects, and never be added merely to fill silence.

Not every category is required in every animation. Silence can be intentional, but must be a documented creative decision.

## 3. Audio production stages

1. **Picture lock:** identify the exact approved video, frame rate, duration, frame range, start timecode and any remaining visual changes. Do not begin final sync against an unstable edit.
2. **Audio spotting:** watch the whole animation and create a cue sheet with timestamps, visible action, sound cue, duration, intensity, pan/movement and source/license.
3. **Asset research and creation:** prioritize original recordings or original synthesis, then clearly licensed free assets. Use only assets whose license and permitted use can be verified. Prefer CC0 or an explicit royalty-free license compatible with the intended release. Record creator, source URL, exact license, download date and attribution requirements. Never assume that “free download” means unrestricted use. No ripped music, copyrighted film/game audio, unlicensed samples or paid assets without approval.
4. **Sound design:** create realistic core effects first, then add restrained cinematic layers. Match sound envelope, pitch, speed, distance, perspective and timing to the visible action.
5. **Music selection/composition:** use original music or a verified license-compatible track. Record its source and license. Avoid vocals/lyrics unless specifically approved. Choose a track that fits the animation's duration and emotional arc; edit with musical phrasing rather than arbitrary chopping.
6. **Edit and synchronize:** work at the animation's exact frame rate. Use frame/timecode-based cue placement. Account for source offsets, fades, tail length and encoder delay. Keep dialogue (if any), effects, ambience and music on separate tracks/stems.
7. **Mix:** establish hierarchy (important action > ambience > music), remove clipping, manage low-frequency masking, use EQ/compression only when helpful, use stereo positioning intentionally, and apply smooth fades. Keep a clean master and separate stems.
8. **Technical QC:** listen on headphones and ordinary speakers; inspect start/end, sync, clipping, noise, abrupt cuts, channel balance, codec, sample rate, channel count and exact duration. Confirm video and audio durations align.
9. **Export and archive:** retain the silent visual master, editable project/timeline, source assets, cue sheet, license manifest, stems, final mix and final muxed video. Never replace a historical preview; version every new output.
10. **Independent review:** ChatGPT reviews the rendered video with audio, cue sheet, technical metadata and license manifest before the result is marked approved.

## 4. Default deliverables per animation

- `<project>_audio_plan.md` — creative direction, spotting notes and cue sheet.
- `audio/assets/` — source audio files, with clear filenames and no unlicensed content.
- `audio/licenses.md` — asset source, creator, license, URL, download date and attribution text.
- `audio/stems/` — engine/effects, ambience, cinematic accents and music stems where practical.
- `audio/mix_preview.wav` or equivalent lossless preview.
- `<project>_sound_preview.mp4` — low-cost video with the draft mix.
- `<project>_final_audio.wav` — final lossless stereo mix.
- `<project>_final.mp4` — final picture + audio.
- `audio_qc.md` — sync, loudness/peak, clipping, duration, codec and listening-test evidence.
- A screen recording documenting the sound-design/editing preview workflow, published beside the corresponding test preview.

## 5. Technical defaults

- Match the picture frame rate exactly; use frame-accurate cue placement.
- Work at 48 kHz for video post-production unless a source workflow requires otherwise.
- Use 24-bit PCM WAV for intermediate/master audio where supported; AAC in MP4 for delivery.
- Stereo delivery by default; preserve mono sources as mono until spatialized intentionally.
- Avoid clipping. Keep true peak at or below -1 dBTP for the final delivery mix unless a specific delivery specification requires otherwise.
- Use integrated loudness appropriate to the destination. For general web video, target approximately -16 LUFS integrated as a starting point, then use listening judgement; do not crush dynamic range merely to hit a number.
- Fade in/out intentionally and ensure the soundtrack does not end abruptly.
- Preserve the original silent render unchanged.
- Use lightweight tools and codecs suitable for the studio workstation. Prefer existing FFmpeg; do not install paid software or add dependencies without approval.

## 6. Pole Drift — first application

**Picture:** 15 seconds, 24 fps, 360 frames, landscape. The exact approved visual render must be confirmed before final synchronization. The known preview is 640×360 H.264; do not assume it is the final picture if a newer approved render exists.

### Sound concept
Nighttime street/track drift: close, punchy and exciting, with a believable car perspective and a restrained electronic/cinematic music bed.

### Required cue families
- Engine: start/idle or approach tone if supported by the picture, rising revs during acceleration, sustained high load through the drift, pitch/level changes with distance, and a natural receding tail.
- Tires: tire squeal/skid layer during the sustained drift, varying intensity with the car's slip and proximity; avoid a constant loop that ignores the animation.
- Surface: subtle tire scrub/gravel/asphalt texture and occasional light debris/skid accents only where visually justified.
- Movement: approach and pass-by/Doppler-style movement only when the camera/car relationship supports it; do not fake a pass-by if the picture does not show one.
- Environment: subtle nighttime outdoor ambience and restrained wind/air tone.
- Cinematic accents: sparse low-impact transitions or whooshes to emphasize entrance, strongest drift moment and exit; no trailer-style overuse.
- Music: original or license-verified electronic/cinematic instrumental, no vocals by default. Build a small arc across the 15 seconds and resolve cleanly at the exit.

### Timing and perspective
Create a frame-accurate cue sheet after watching the current approved picture. Do not invent exact cue times in advance. Track the car's screen position and apparent distance; pan and automate level/pitch only when justified. Keep tire squeal subordinate to the engine and music; keep music below the key action sounds.

### First-pass workflow
1. Inspect local and GitHub project files; identify the latest approved visual render and its matching editable .blend. Do not modify animation, camera, lighting, geometry or historical outputs.
2. Watch the entire picture and create `pole_drift_audio_plan.md` with a frame/timecode cue sheet.
3. Source or create the sound layers and music. Verify and document every license before use. If a license cannot be verified, do not use that asset.
4. Build a non-destructive audio timeline/project with separate tracks/stems.
5. Export a draft stereo mix and mux it with a low-resolution copy of the exact picture. Keep the silent master untouched.
6. Run technical QC and listen to the whole result. Create a matching screen recording of the sound-design workflow.
7. Update the root `current report.md` with files, sources/licenses, cue-sheet summary, toolchain, test evidence, duration/sync and known issues.
8. Stop for ChatGPT review. Do not call the soundtrack final, publish it as approved, or replace the silent master until ChatGPT approves it.
9. After approval, render the final audio mix, mux the final video, archive stems and licenses, and add the audio-enabled preview/final video plus screen recording to the chronological README gallery.

## 7. Rights and release safety

A soundtrack is not release-ready without a source/license record for every non-original asset. Preserve required attribution in the project and public release notes. Do not use a source merely because it is downloadable. Where a platform's license or terms are unclear, reject the asset and find a clearer alternative.

## 8. GitHub and reporting rules

- GitHub is the canonical source of truth.
- **No local commits and no local pushes.** Antigravity may build and test locally but must not run `git commit` or `git push`. ChatGPT publishes reviewed documentation/artifacts directly to GitHub.
- Antigravity updates root `current report.md` after every meaningful task.
- Every audio/video preview or test render and its corresponding screen recording must be uploaded and added to the README gallery with a description, settings, and status.
- Preserve historical previews and the silent master.
- Never modify `projects/integration-smoke-test/`.
