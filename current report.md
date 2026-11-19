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
