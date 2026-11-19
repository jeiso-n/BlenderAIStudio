# Current Report — Blender AI Animation Studio

**Last updated:** 2026-11-19
**Current phase:** First animation production preview and studio workflow validation
**Status:** Blender–Antigravity integration smoke test passed. Pole Drift preview rendered and technically verified; visual corrections remain before final approval. GitHub gallery documentation is being maintained through remote-only commits.

## Latest update — GitHub video gallery publication check (2026-11-19)
- Repository: https://github.com/jeiso-n/BlenderAIStudio
- Verified remote branch head before this documentation update: `64d1ba9f4b807561a2a78541010806d77bd6ed88`.
- Verified integration smoke-test artifacts in `projects/integration-smoke-test/`:
  - `animation.mp4` — 286,756 bytes; H.264, 540×960, 24 fps, 120 frames, 5 seconds.
  - `test 1 screen recording.mp4` — 18,050,712 bytes.
  - `integration_smoke_test.blend` — 149,367 bytes.
  - `preview.png` — 573,785 bytes.
  - `production_notes.md` — present.
- The integration screen recording is now confirmed on GitHub. The rendered integration MP4 and editable project assets were already present remotely.
- **Pole Drift publication is still pending:** GitHub currently has no `projects/pole-drift/` directory. The local `preview.mp4` and `pole drift screen recording.mp4` have not been verified on GitHub. Do not publish links or claim these files are uploaded until the remote directory listing confirms them.
- README now includes a chronological Animation Preview & Test Gallery, with the integration test linked and Pole Drift clearly marked as awaiting binary upload. No broken or speculative Pole Drift links are included.
- This documentation checkpoint is created directly on GitHub. No local commit or push is used.

## Project roles and operating rules
- Project owner / Creative Director: owns creative direction and approves scope.
- ChatGPT: chief architect, production planner, independent reviewer, and quality gate. ChatGPT is not the implementation agent.
- Antigravity: lead builder and Blender-operation agent.
- Gemini / GitHub Copilot: supporting implementation assistants.
- Blender: actual 3D production engine (modeling, materials, rigging, animation, lighting, cameras, rendering). This is not an AI-video-generation project.
- GitHub repository: https://github.com/jeiso-n/BlenderAIStudio
- **GitHub is the sole source of truth. All commits must be created directly on GitHub. Do not run local `git commit` or create local-only commits on the user's computer.** Use GitHub API / GitHub web operations for remote commits. Do not push local commits.
- Every meaningful development task must update this root `current report.md` with files changed, tests, evidence, limitations, and next step.
- ChatGPT independently reviews Antigravity's report and outputs before accepting completion.
- Every preview/test render and its matching screen recording must be published and listed in the README gallery with project, description, settings, and status.

## Verified workstation
- OS: Windows 11 Home, build 26300, 64-bit.
- CPU: AMD Ryzen 5 5500U, 6 cores / 12 logical processors.
- Usable RAM: 7.3 GB.
- GPU: integrated AMD Radeon graphics; Windows reports 512 MB dedicated adapter memory.
- Free disk at initial audit: C: approximately 76.2 GB; D: approximately 192.8 GB.

## Installed tools
| Tool | Verified version / state |
|---|---|
| Blender | 5.3.0 at `C:\\Program Files\\Blender Foundation\\Blender 5.3` |
| BlendRelay MCP | 0.7.8; Blender extension installed and enabled |
| uv / uvx | 0.13.9 |
| Antigravity CLI | `agy` 1.5.11 |
| Antigravity IDE | editor build 1.107.0 |
| Python | 3.13.17 |
| FFmpeg | 9.0.1 Essentials |
| Git | 2.56.0.windows.4 (installed; local commits are prohibited by project workflow) |

## Antigravity ↔ Blender connection
- BlendRelay MCP is configured in Antigravity's global config at `%USERPROFILE%\\.gemini\\config\\mcp_config.json`; the existing `agent-desktop` entry was preserved.
- BlendRelay diagnostic: PASS, zero errors and zero warnings.
- Antigravity successfully invoked BlendRelay `get_scene_info` against a live Blender 5.3.0 session (instance `33b0e99b1b7c46a8a0d72916242c7c7f`).
- Initial read-only scene inspection returned Scene, active Camera, engine `BLENDER_EEVEE`, and three visible objects: Cube, Light, Camera.
- The Antigravity Manage MCP panel had a persistent loading issue; agent-side tool invocation nevertheless proved the live integration.

## First end-to-end production test — Integration Smoke Test
**Result: PASS.** Antigravity created a real Blender scene through BlendRelay, saved an editable project, rendered a still and a video, and verified keyframes and output metadata.

Location: `projects/integration-smoke-test/`
- `integration_smoke_test.blend` — editable Blender project (149,367 bytes at local verification; now confirmed remotely).
- `preview.png` — rendered 540×960 still (573,785 bytes at local verification; now confirmed remotely).
- `animation.mp4` — H.264, 540×960, 24 fps, 120 frames, 5.000 seconds (286,756 bytes; now confirmed remotely).
- `test 1 screen recording.mp4` — 18,050,712 bytes; now confirmed remotely.
- `production_notes.md` — scene construction and render details; present remotely.

Scene: dark studio, metallic pedestal, rotating metallic icosahedron, counter-rotating pink ring, two-line 3D title, warm/cyan/magenta area lights, portrait camera.
Render: Eevee `BLENDER_EEVEE`, 24 samples, 540×960, 24 fps, frames 1–120. Preview approximately 5 seconds; animation approximately 300 seconds.
Verification: Blender keyframes read back; active camera and render settings checked; FFprobe independently confirmed H.264, 540×960, 24 fps, 120 frames, 5.000 seconds. Screen recording and rendered MP4 are present in the remote repository.
Limitations: no motion blur; title uses scale/rise rather than fade; low resolution and samples are intentional for current hardware. Animation rendered with Blender CLI from the saved file. The default Blender startup file was not overwritten, but the open GUI document was replaced with the test scene.

## First production animation — Pole Drift
**Result: PREVIEW RENDERED; NEEDS FIXES before final rendering.**

Location expected: `projects/pole-drift/`
- `preview.mp4` — local preview, 640×360, 24 fps, 360 frames, 15 seconds, H.264; remote upload not yet verified.
- `preview.png` — preview still (frame 110).
- `pole_drift.blend` — editable scene.
- `build_pole_drift.py` — scene rebuild script.
- `production_notes.md` — production details.
- `render_pole_drift.py` and `verify_pole_drift.py` — render and verification scripts.
- `pole drift screen recording.mp4` — local screen recording; remote upload not yet verified.

Scene: low-poly orange sports car with body, cabin, spoiler, lights, four wheels with steering/spin, roll/bounce; nighttime asphalt pad and illuminated pole; skid marks and stylized tire smoke.
Motion: enters from left, performs two laps around a 6.2m circle at approximately 36–40° slip, then arcs out and recedes.
Geometry: 5,364 triangles.
Render: Eevee, 8 samples, 24 fps, frames 1–360. Render time approximately 712 seconds.
Technical verification: FFprobe reported H.264, 640×360, 24 fps, 360 frames, 15 seconds. Headless reopen of the saved `.blend` passed; keyframes were present on car, wheels, and camera rig; car remained in view during the main drift; no position jumps; car remained grounded and wheels rolled forward.
Independent review decision: NEEDS FIXES before final render:
1. Car approaches the frame edge near 8 seconds.
2. Exit car recedes but remains visible at frame 360.
3. Wheels are partly embedded in the body sides; improve placement / wheel-arch treatment.
4. Smoke puffs are faceted and need a more coherent visual treatment.
Do not render final 1280×720 output until a corrected preview is independently approved.

## Rendering guidance
- Workstation is constrained (7.3 GB usable RAM and integrated graphics).
- Start with Eevee, simple geometry, modest texture sizes, low sample counts, and reduced-resolution previews.
- Use 360×640 or 540×960 for portrait previews, and 640×360 for landscape previews.
- Avoid heavy simulations, dense geometry, large texture libraries, and high-sample photorealistic rendering until benchmarked.

## GitHub migration and publication policy
- Repository: `jeiso-n/BlenderAIStudio`.
- GitHub is the canonical source of truth. No local commits and no local pushes.
- The README contains the chronological Animation Preview & Test Gallery.
- Verify every binary file through the GitHub remote tree / contents listing before linking it or marking it published.
- Do not modify the integration smoke-test regression fixture.
- Next publication step: upload both Pole Drift video files to `projects/pole-drift/`, then update the README gallery with direct links and update this report with remote file sizes / verification.
- After the Pole Drift corrective pass, publish the corrected preview and its matching screen recording as a new chronological gallery entry; retain the original preview as history.


## Latest update — Pole Drift files verified on GitHub (2026-11-19)
The owner uploaded the Pole Drift project files to the repository root-level `pole-drift/` directory (not `projects/pole-drift/`). The remote GitHub contents listing confirms:
- `pole-drift/preview.mp4` — 703,893 bytes; the 15-second 640×360, 24 fps H.264 preview.
- `pole-drift/pole drift screen recording.mp4` — 20,964,843 bytes; corresponding production screen recording.
- `pole-drift/pole_drift.blend` — 250,730 bytes; editable Blender scene.
- `pole-drift/build_pole_drift.py` — 23,528 bytes.
- `pole-drift/production_notes.md` — 4,503 bytes.
- `pole-drift/render_pole_drift.py` — 960 bytes.
- `pole-drift/verify_pole_drift.py` — 5,704 bytes.
- `pole-drift/preview.png` — 224,610 bytes.
- `pole-drift/review_contact.png` — 355,208 bytes.
- `pole-drift/pole_drift.blend1` — 250,709 bytes (Blender backup file; retained as uploaded).

README gallery links now use the actual root-level paths and both videos are verified present. No files were moved or renamed. The earlier statement that Pole Drift upload was pending is superseded by this update. The review decision remains NEEDS FIXES before final render: improve camera-edge clearance, exit framing, wheel placement, and smoke treatment. The documentation checkpoint is created directly on GitHub; no local commit or push.



## Latest update — Studio audio production standard established (2026-11-19)

**Decision:** The Creative Director approved a hybrid sound identity with background music enabled by default. This is now the studio-wide default for all animations, unless an intentional silence exception is documented.

- Added the canonical standard at `docs/AUDIO-PRODUCTION-STANDARD.md`.
- Defined the audiovisual workflow: picture lock → audio spotting/cue sheet → license-verified asset sourcing or original creation → sound design → music → frame-accurate edit → mix → technical/listening QC → archive → independent ChatGPT review.
- Defined rights management: every external asset must have a recorded creator, source URL, exact license, download date and attribution requirement. Unclear or incompatible licenses are rejected.
- Defined default delivery: preserve the silent visual master; archive project/timeline, stems, lossless mix, license manifest and final muxed video. Keep previews versioned and publish each test preview with its corresponding screen recording in the README gallery.
- Technical starting points: 48 kHz, 24-bit PCM intermediates where supported, stereo delivery, no clipping, true peak at or below -1 dBTP, and approximately -16 LUFS integrated as a web-video starting point (subject to listening and destination requirements).
- Pole Drift is the first application. Antigravity must identify the latest approved 15-second, 24 fps picture, create a frame-accurate cue sheet, build realistic engine/tire/environment layers plus restrained cinematic accents and licensed/original electronic music, then produce a draft mix and audio-enabled preview for review.
- No final audio or public approval is implied by this documentation update. The actual soundtrack, asset licenses, sync, mix and export remain to be built and reviewed.
- Antigravity must not alter the approved visual animation or overwrite historical files. No local commits/pushes; GitHub remains canonical and ChatGPT publishes reviewed work remotely.

ChatGPT independently reviews `pole_drift_sound_preview.mp4`, `pole_drift_audio_plan.md`, `audio/licenses.md`, `audio_qc.md`, and `pole_drift_audio_workflow_viz.mp4` before proceeding to final mastering.
# Current Report — Blender AI Animation Studio

**Last updated:** 2026-11-19  
**Workstream:** Environment setup and Blender–Antigravity integration  
**Status:** Core tools installed; restart and live UI handshake remain.

## Verified machine

- OS: Windows 11 Home, build 26300, 64-bit
- CPU: AMD Ryzen 5 5500U, 6 cores / 12 logical processors
- Usable RAM reported by Windows: 7.3 GB
- GPU: AMD Radeon integrated graphics; Windows reports 512 MB dedicated adapter memory
- Free disk space at audit: C: 76.2 GB; D: 192.8 GB

## Installed and verified tools

| Tool | Verified version / state |
|---|---|
| Blender | 5.3.0, installed at `C:\Program Files\Blender Foundation\Blender 5.3` |
| BlendRelay MCP | 0.7.8 installed for Blender 5.3; add-on enabled in saved Blender preferences |
| BlendRelay diagnostics | PASS — 0 errors, 0 warnings |
| uv / uvx | 0.13.9 installed with WinGet; user PATH updated |
| Antigravity CLI | `agy` 1.5.11 already installed; user PATH updated |
| Antigravity IDE command | `antigravity-ide` reports editor build 1.107.0 |
| Python | 3.13.17 |
| FFmpeg | 9.0.1 Essentials build |
| Git | 2.56.0.windows.4 |

## Antigravity integration

- Created `%USERPROFILE%\.gemini\antigravity\mcp_config.json` with a `blendrelay` MCP server entry.
- MCP command points to the installed absolute `uvx.exe` path to avoid PATH-refresh issues.
- Existing MCP config was absent, so no prior server settings were overwritten.
- Blender extension module `bl_ext.user_default.blendrelay_mcp` was enabled and preferences saved.

## Rendering smoke test

- Blender background render completed successfully with Eevee at 320 × 320.
- Blender 5.3 exposes the Eevee engine identifier as `BLENDER_EEVEE` on this installation; the earlier `BLENDER_EEVEE_NEXT` identifier was not accepted and was corrected.
- Outputs: `%TEMP%\BlenderAIStudio_SetupSmokeTest\smoke_test.png` and `smoke_test.blend`.
- Render completed in approximately 18.45 seconds on this machine.

## Performance constraints and production defaults

- Treat this as a constrained workstation: 8 GB-class RAM and integrated graphics.
- Start with Eevee, simple geometry, modest texture sizes, low sample counts, and low-resolution previews.
- Avoid heavy simulations, large texture libraries, dense geometry, and high-sample photorealistic rendering until tested.
- Social-video target can remain vertical 1080 × 1920 at 30 fps for final export, but previews should be reduced (for example 360 × 640 or 540 × 960).

## Remaining activation checks

1. Restart Blender so the already-enabled extension loads in the open GUI session.
2. Restart Antigravity IDE so it reloads the new MCP server configuration.
3. In Blender, open the 3D Viewport sidebar with `N`, choose **BlendRelay**, and click **Connect**.
4. Confirm Antigravity can see the BlendRelay MCP tools and perform a read-only scene inspection before any scene edits.
5. Confirm the Antigravity CLI's first-run authentication if prompted; only the CLI version has been verified so far.

## Scope boundaries

- Blender, Python, FFmpeg, Git, uv, and Antigravity CLI are installed or verified; no duplicate Python or Blender installation was added.
- No optional asset packs, audio editors, paid services, or unrelated AI agents were installed.
- Project source scaffold and Git repository initialization have not yet been started; Antigravity remains the implementation agent for that phase.
- No credentials or secrets are stored in this report.

## Post-restart verification — 2026-11-19

- User confirmed Blender and Antigravity are both open.
- Remote process inspection confirms Blender 5.3.0 GUI process is running.
- Blender background preference check confirms `bl_ext.user_default.blendrelay_mcp` remains enabled.
- Antigravity CLI process `agy` is running; MCP config remains present.
- `blendrelay-mcp doctor` rerun after restart: PASS, 0 errors, 0 warnings.
- **Not yet proven:** the user has not yet confirmed clicking Connect in Blender's BlendRelay sidebar, and Antigravity has not yet demonstrated a live scene-inspection request. Do not mark integration complete until that handshake is tested.


## BlendRelay Connect troubleshooting — 2026-11-19

- Inspected the installed add-on source rather than guessing from the UI.
- The Connect / Refresh operator creates a local socket connection and reads `connection.json`; it does not launch the runtime itself.
- Blender's default runtime root is `%LOCALAPPDATA%\\BlendRelayMCP`.
- That folder currently contains workspace data but no `connection.json`, confirming the runtime gateway has not initialized yet.
- Antigravity IDE and its `agy --hub` process are running. No BlendRelay MCP server process was observed in the process list.
- Both candidate Antigravity CLI paths exist, so the previously suspected path mismatch is not established as the cause.
- Current diagnosis: Antigravity has not yet started/loaded the BlendRelay MCP server (or invoked a BlendRelay tool); the Blender Connect button alone cannot start the runtime.
- Next verification: inspect Antigravity's MCP server list/status and confirm whether `blendrelay` is listed and running; then invoke a read-only BlendRelay tool to initialize the runtime and retry Connect.
- No configuration files were changed during this diagnostic pass.


## Antigravity MCP manager investigation and config-path correction — 2026-11-19

- User screenshot shows Antigravity Manage MCP servers stuck at “Loading MCP servers…” / “Refreshing…”.
- The existing config at `%USERPROFILE%\\.gemini\\antigravity\\mcp_config.json` parsed as valid JSON and contained BlendRelay only.
- Local `uvx 0.13.9` and `uvx blendrelay-mcp doctor` both execute successfully; BlendRelay 0.7.8 diagnostic PASS (0 errors, 0 warnings).
- Found an existing newer global config at `%USERPROFILE%\\.gemini\\config\\mcp_config.json` containing an `agent-desktop` MCP entry. Preserved it.
- Updated the newer global config by merging in the BlendRelay server entry, using the verified absolute uvx.exe path and `timeoutSeconds: 300`. Existing old Antigravity config was left untouched as backup; no other server entries were removed.
- Web documentation currently identifies `~/.gemini/config/mcp_config.json` as Antigravity IDE's global config path. The previous setup had only populated the legacy `~/.gemini/antigravity/mcp_config.json` path.
- An exact-match Google Antigravity community report documents the Manage MCP servers page remaining forever on “Loading MCP servers…” in Antigravity IDE 1.107.0, even with empty config; this may be a separate UI defect. The page itself is not a reliable test of whether the agent can load MCP tools.
- Next step: reload Antigravity window so it reads the newer global config, then test a read-only BlendRelay tool through the agent. If Manage MCP UI remains stuck, treat that UI as a separate bug and continue validating via agent tool calls/logs.


## BlendRelay live connection verified — 2026-11-19

- Antigravity agent successfully reported BlendRelay MCP server available and connected to a live Blender session.
- BlendRelay version: 0.7.8.
- Blender instance ID: `33b0e99b1b7c46a8a0d72916242c7c7f`.
- Read-only `get_scene_info` call succeeded.
- Scene: `Scene`; active camera: `Camera`; render engine: `BLENDER_EEVEE`.
- Three visible objects confirmed: Cube (MESH at [0,0,0]), Light (LIGHT at [4.076,1.005,5.904]), Camera (CAMERA at [7.359,-6.926,4.958]).
- No Blender scene changes were made during this connection verification.
- This proves the Antigravity-to-BlendRelay-to-Blender read path. It does not yet prove object creation/modification, keyframing, saving a .blend, rendering, or artifact retrieval.
- Next milestone: controlled end-to-end integration smoke test in a new project file, preserving the user's default startup scene. Create a simple lightweight animated 3D scene, save the .blend, render a preview PNG, verify the output, then record evidence and commit a checkpoint.

## Integration smoke test (2026-11-19)

**Result: PASS** (all four outputs generated and verified).

Files in `projects/integration-smoke-test/`: `integration_smoke_test.blend` (149,367 B), `preview.png` (573,785 B, 540x960), `animation.mp4` (286,756 B), `production_notes.md`.

Blender operations (via BlendRelay `execute_blender_python`): cleared session scene, created Studio collection, floor/backdrop/pedestal, hero icosahedron + ring, 3D title, 3 area lights, camera with track-to, materials, keyframes + interpolation, render/H.264 settings, `save_as_mainfile`. Read-only checks via `get_scene_info`.

Render settings: Eevee `BLENDER_EEVEE`, 24 samples, 540x960, 24 fps, frames 1-120, H.264 MP4. Durations: preview ~5 s render; animation ~300 s (299.8 s wall-clock).

Verification evidence: keyframe counts read back (hero/ring rotation 2 keys per channel + 3 location keys; title 2 keys per channel); active camera `Camera`; engine/resolution/fps read back; ffprobe: h264, 540x960, 24/1 fps, 120 frames, 5.0 s; preview inspected visually.

Issues: `FFMPEG` file_format needs `media_type='VIDEO'` in Blender 5.3 (fixed). `D:\AI-Operations-Vault\START-HERE.md` was not found, so the vault could not be consulted. The project folder was not a Git repo; a local one was initialised. Not pushed (no remote, no permission).


## Independent review by ChatGPT — 2026-11-19

**Current milestone status: PASS — first real Blender animation generated and committed locally.** This section supersedes earlier status lines above that say the live handshake or integration smoke test remain pending.

Independent checks performed against the local machine and repository:
- Confirmed all four deliverables exist in `projects/integration-smoke-test/`: `integration_smoke_test.blend`, `preview.png`, `animation.mp4`, and `production_notes.md`.
- Confirmed actual file sizes at inspection: blend 149,367 bytes; preview 573,785 bytes; MP4 286,756 bytes; notes 1,561 bytes.
- Ran FFprobe independently against `animation.mp4`: H.264, 540x960, 24/1 fps, 120 frames, 5.000 seconds.
- Confirmed Blender executable reports version 5.3.0.
- Confirmed Git repository root is `D:/Projects/BlenderAIStudio`, branch `main`, and HEAD is `f95a169` (`test(integration): add BlendRelay end-to-end smoke test project and outputs`). The deliverables and report are tracked in that commit.
- Confirmed working tree was clean at inspection. No Git remote is configured. No push was made.
- The nested integration-smoke-test folder is part of the root repository; it is not a separate Git repository. The root commit is the checkpoint.

Review notes:
- File existence, saved project, image dimensions (as reported by production notes), and video encoding/duration are verified. The full visual composition and animation playback have not yet been independently inspected by ChatGPT; visual quality is therefore accepted provisionally based on Antigravity's preview inspection and notes.
- The default Blender startup file was not overwritten. The currently open GUI document was intentionally replaced with the test scene, as disclosed by the builder.
- Next phase should be production-foundation architecture and a small reusable asset/animation pipeline, not another connectivity test. Preserve this working smoke-test project as a regression fixture.
- Before further implementation, Antigravity should refresh the top-of-file status summary and remove or mark superseded statements in earlier sections so `current report.md` presents one coherent current state.

## Pole Drift — low-resolution preview build (2026-11-19)

**Status:** Preview built and verified by the builder; awaiting ChatGPT's independent review. Final 720p NOT rendered. No commits made, nothing pushed.

### Files (all in `D:\Projects\BlenderAIStudio\projects\pole-drift\`)
- `build_pole_drift.py` (rerunnable build), `render_pole_drift.py` (render helper), `verify_pole_drift.py` (headless checks)
- `pole_drift.blend` (250,730 B), `preview.mp4` (703,893 B), `preview.png` (224,610 B, frame 110), `production_notes.md`
- `pole_drift.blend1` is Blender's automatic backup (git-ignored).
- `projects/integration-smoke-test` untouched (`git diff` empty).

### Architecture / approach
Car hierarchy `Car_Root` (path+yaw) → `Car_Chassis` (roll/pitch/bounce) → low-poly body mesh; four wheels with steer + spin empties. Motion is a closed-form function of time (circle R=6.2 m, 90°/s, 9.74 m/s, 36-40° slip angle), keyed every frame. Skid marks are ribbons built from the exact rear-wheel paths and revealed with Build modifiers; 118 shared-mesh smoke puffs (keyframed scale/position, no simulation). Four lights (pole point, cyan rim, blue fill, car spot). Full details in `production_notes.md`.

### Render settings and measurements
Eevee, 640×360, 24 fps, frames 1–360, 8 samples, no motion blur, H.264 MP4. Full 360-frame render: 712 s Blender render time (721 s wall clock, ~2 s/frame). Observed Blender working set up to ~2.3 GB (2,395,648,000 B; my peak-tracking command had an Int32 bug, so the printed 1982 MB is not reliable). Single still ≈ 3.6 s. Scene: 5,364 triangles (limit 20,000), 153 objects.

### FFprobe (preview.mp4)
h264 High, yuv420p, 640×360, 24/1 fps, 360 frames counted, duration 15.000000 s.

### Quality checks (builder results; not ChatGPT approval)
`verify_pole_drift.py` re-opens the saved .blend headless: OVERALL PASS — engine/fps/range/resolution/samples; keyframes on car, chassis, wheels, camera rig; car in camera view for all frames 73–265; max step 0.406 m/frame (no jumps); max yaw step 5.0°/frame; min car–pole gap 3.81 m; car z = 0; slip angle 36.1–39.7°; wheels roll forward; front wheels steer −32°. Visually inspected stills at frames 1, 20, 45, 100, 110, 150, 200, 250, 280, 330, 345, 360 and an extracted MP4 frame at 8 s.

### Known issues
- Car is close to the frame edge on the near side of the circle (e.g. ~8 s) and near the right edge around frames 200–330; whole car stays in view during the main drift per the check.
- Car recedes and is still a small figure in frame at frame 360 (does not leave the frame).
- Smoke puffs are faceted, stylised hexagon-like shapes; light beam is a cheap transparent cone.
- Wheels are partly embedded in body sides (no wheel arches). Low resolution/samples by design.
- Initial default state: `Material.use_nodes` deprecation warnings (harmless in 5.3).

### Git status
Branch `main`, 0 ahead / **4 behind** `origin/main` (fetch only; no pull/merge/reset). Remote has commits 640d43f, f7a57e5, 3b42ffa, b6e0b98 (README, report and smoke-test notes updates) not present locally, so this local `current report.md` is an older version and differs from GitHub's. `projects/pole-drift/` is untracked. No commits, no pushes. Local report was appended to only; ChatGPT should reconcile it with the GitHub version.

### Next recommended step
ChatGPT reviews `preview.mp4`/`preview.png`; if approved, render 1280×720 at 16 samples (estimated ~3× the preview time, ~35 min) via `blender -b pole_drift.blend` after changing resolution/samples in the build script.

## Pole Drift — audio production preview (2026-11-19)

**Status:** Draft audio preview built and verified by the builder; awaiting ChatGPT's independent review before final mastering. No commits made, nothing pushed. Note: `docs/AUDIO-PRODUCTION-STANDARD.md` and `README.md` were not present in the local working tree (local repo is 4 commits behind `origin/main` as noted above), so the assignment's explicit studio standard (hybrid sound identity with background music enabled) was followed.

### Selected visual master (picture lock)
- **Video:** `D:\Projects\BlenderAIStudio\projects\pole-drift\preview.mp4` (703,893 B) — `640x360`, `24/1 fps`, `360` frames, `15.000000 s`, H.264 High (`yuv420p`), silent. Confirmed as the only Pole Drift render on disk; preserved untouched.
- **Editable `.blend`:** `D:\Projects\BlenderAIStudio\projects\pole-drift\pole_drift.blend` (277,654 B) and `build_pole_drift.py` (23,528 B) — untouched.

### Files created (all in `D:\Projects\BlenderAIStudio\projects\pole-drift\`)
- `pole_drift_audio_plan.md` (8,138 B) — frame-accurate cue sheet (frames 1–360, 0.00–15.00 s) mapped to `car_state(t)` and `cam_pos(t)`
- `audio/build_audio.py` (21,742 B) — reproducible Python 3.13 + FFmpeg synthesis, spatialization, and mixing pipeline
- `audio/licenses.md` (2,775 B) — asset license manifest
- `audio/assets/` — 5 original 48 kHz / 16-bit stereo raw assets (`engine_raw.wav`, `tires_raw.wav`, `env_raw.wav`, `cinematic_raw.wav`, `music_raw.wav`; 2,880,044 B each)
- `audio/stems/` — 5 mastered stereo stems (`01_engine.wav` 2,894,478 B, `02_tires.wav` 2,890,638 B, `03_environment.wav` 2,880,078 B, `04_cinematic.wav` 2,910,798 B, `05_music.wav` 2,901,198 B)
- `audio/mix_preview.wav` (2,894,478 B) — 5-stem stereo master preview mix
- `pole_drift_sound_preview.mp4` (1,071,727 B) — `preview.mp4` (`-c:v copy`) + `audio/mix_preview.wav` (AAC 192 kbps)
- `pole_drift_audio_workflow_viz.mp4` (4,664,775 B) — synchronized side-by-side preview + real-time stereo waveform & spectrum diagnostic
- `audio_qc.md` (4,248 B) — full QC report

### Audio sources & licenses
100% original procedural synthesis and FFmpeg signal processing created in `audio/build_audio.py` (Original Studio Creation / CC0-equivalent, zero third-party or copyrighted assets).

### Cue sheet & mixing summary
- **Spatialization:** Inverse-distance attenuation (`14.0 m` min foreground to `42.1 m` entry/exit), Doppler pitch shift (`343 / (343 + v_rad)`), behind-pole air absorption, and equal-power stereo panning (`-0.88` left entry -> `-0.45..+0.46` foreground sweeps -> `+0.49` upper-right exit).
- **Timeline:** Intro rumble & night wind (`0–1.9 s`), turn-in & skid onset (`2.2–3.0 s`, skid marks `f61` = `2.50 s`), 2-lap circular drift with sustained engine load, dual-formant tire squeal & 124 BPM D-minor dark-synthwave drop (`3.0–12.4 s`, Lap 1 peak accent `7.25 s`), controlled exit & chord resolution (`12.4–15.0 s`).
- **Export settings:** 48 kHz, 16-bit PCM WAV stems/mix; `pole_drift_sound_preview.mp4` uses `-c:v copy` (640×360, 24 fps H.264) + `-c:a aac -b:a 192k -ar 48000 -ac 2`.

### QC results (builder measurements; awaiting ChatGPT review)
- **Mix loudness & peak (`ebur128` + `volumedetect`):** Integrated `-15.2 LUFS`, True Peak `-2.9 dBFS`, Max `-2.9 dB`, Mean `-18.0 dB`, zero clipping.
- **Stem balance:** `01_engine` `-18.4 LUFS`, `02_tires` `-20.6 LUFS`, `03_environment` `-36.9 LUFS`, `04_cinematic` `-25.6 LUFS`, `05_music` `-24.2 LUFS` (sidechain-ducked under `01_engine + 02_tires`).
- **`ffprobe pole_drift_sound_preview.mp4`:** Video `h264 (High)`, `640x360`, `24/1 fps`, `360` frames, `15.000000 s`; Audio `aac (LC)`, `48000 Hz`, `stereo`, `193,195 bps`.

### Known problems
- `ffmpeg -f gdigrab` failed with Windows error `5` (Access Denied) in the headless agent shell, so a live desktop screen recording could not be captured; `pole_drift_audio_workflow_viz.mp4` was rendered as a synchronized audiovisual waveform/spectrum diagnostic instead.
- Vehicle/tire stems are procedural synthesis rather than recorded foley; subjective listening approval by ChatGPT / Creative Director is pending.

### Next recommended step
ChatGPT independently reviews `pole_drift_sound_preview.mp4`, `pole_drift_audio_plan.md`, `audio/licenses.md`, `audio_qc.md`, and `pole_drift_audio_workflow_viz.mp4` before proceeding to final mastering.
