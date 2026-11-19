# Blender AI Animation Studio

An AI-directed 3D animation production studio built around **Blender** and coordinated AI agents. The goal is to turn creative briefs into editable Blender scenes and finished video exports using real 3D production workflows—not AI video generation.

## Project roles
- **Project owner / Creative Director:** defines goals and approves creative direction.
- **ChatGPT:** chief architect, production planner, reviewer, and quality gate.
- **Antigravity:** lead implementation and Blender-operation agent.
- **Gemini / GitHub Copilot:** supporting implementation agents.
- **Blender:** actual 3D engine for modeling, materials, rigging, animation, lighting, cameras, and rendering.
- **GitHub:** canonical source of truth. Development commits are created directly on GitHub; do not create local Git commits.

## Current milestone
**Passed:** Blender 5.3.0 is connected to Antigravity through BlendRelay MCP 0.7.8. The integration smoke test produced an editable Blender scene, still image, and H.264 animation. The first full production animation preview, **Pole Drift**, has also been rendered and technically verified; it remains in review and needs framing/exit/wheel/smoke refinements before final rendering.

See [current report](current%20report.md) for environment details, verification evidence, limitations, and next steps.

## Animation Preview & Test Gallery

This gallery is chronological. Each entry identifies the purpose of the test, its render settings, and its review status. Screen recordings document the corresponding production workflow.

### 1. Blender / BlendRelay integration smoke test
**Status:** Integration test — passed

A first end-to-end check that Antigravity could control a live Blender session through BlendRelay, construct a real 3D scene, save an editable project, and render a video.

- **Rendered video:** [animation.mp4](projects/integration-smoke-test/animation.mp4)
- **Screen recording:** [test 1 screen recording.mp4](projects/integration-smoke-test/test%201%20screen%20recording.mp4)
- **Editable Blender project:** [integration_smoke_test.blend](projects/integration-smoke-test/integration_smoke_test.blend)
- **Preview still:** [preview.png](projects/integration-smoke-test/preview.png)
- **Settings:** Eevee, 540×960 portrait, 24 fps, 120 frames / 5 seconds, 24 samples, H.264.
- **Scene:** rotating metallic icosahedron and counter-rotating ring on a lit studio pedestal, with 3D title and colored studio lighting.

### 2. Pole Drift — first production preview
**Status:** Preview rendered; awaiting corrective pass and independent visual approval

A low-poly sports car enters a nighttime drift arena, circles an illuminated pole in a sustained drift, and begins its exit. This is the first full production animation preview beyond the integration fixture.

- **Rendered video:** [preview.mp4](pole-drift/preview.mp4)
- **Screen recording:** [pole drift screen recording.mp4](pole-drift/pole%20drift%20screen%20recording.mp4)
- **Editable Blender project:** [pole_drift.blend](pole-drift/pole_drift.blend)
- **Preview still:** [preview.png](pole-drift/preview.png)
- **Production notes:** [production_notes.md](pole-drift/production_notes.md)
- **Render settings:** Eevee, 640×360 landscape, 24 fps, 360 frames / 15 seconds, 8 samples, H.264.
- **Scene:** low-poly orange sports car, illuminated central pole, nighttime asphalt arena, skid marks, stylized tire smoke, cyan/blue ambient accents and warm pole lighting.
- **Review:** technical checks passed; visual corrections are still required for camera-edge clearance, exit framing, wheel placement, and smoke presentation. Do not treat this preview as final.

## Production principles
1. Use real Blender scenes and editable `.blend` files.
2. Keep preview settings practical for the current 8 GB-class RAM / integrated-GPU workstation.
3. Preserve verified work and avoid destructive changes.
4. Update `current report.md` after every meaningful development task.
5. Review outputs and test evidence before declaring a task complete.
6. Create commits directly on GitHub. Never create local commits on the user's computer.
7. Never push or publish unreviewed changes.
8. Publish every animation preview/test render and its corresponding screen recording in this gallery, with a description, settings, and status.

## Repository layout
- `current report.md` — durable project status and verification log.
- `projects/integration-smoke-test/` — first verified Blender production test.
- `pole-drift/` — first full production animation and its published outputs.
- `docs/` — architecture and workflow documentation (to be developed).
- `agents/` — agent roles and orchestration (to be developed).
- `scripts/` — Blender and production automation (to be developed).
- `templates/` — reusable animation templates (to be developed).
- `assets/` — approved reusable assets (to be developed).
- `renders/` — preview and final outputs (to be developed).

## Getting started
Install Blender 5.3 or a compatible supported release, configure BlendRelay MCP for your agent environment, and open the relevant `.blend` project in Blender. Detailed setup and production workflow documentation will be added as the studio foundation is implemented.

## Current constraints
The initial workstation has an AMD Ryzen 5 5500U, 7.3 GB usable RAM, and integrated AMD Radeon graphics. Begin with Eevee, modest geometry, low texture sizes, and reduced-resolution previews. Use higher-resolution final settings only after preview approval and performance checks.
