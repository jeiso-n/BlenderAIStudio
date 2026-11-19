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
**Passed:** Blender 5.3.0 is connected to Antigravity through BlendRelay MCP 0.7.8. A first 5-second vertical 3D animation was generated and verified.

The integration smoke test uses Eevee at 540×960, 24 fps, 120 frames, H.264. The saved `.blend` project, preview image, MP4, and production notes are the initial regression fixture.

See [current report](current%20report.md) for environment details, verification evidence, limitations, and next steps.

## Production principles
1. Use real Blender scenes and editable `.blend` files.
2. Keep preview settings practical for the current 8 GB-class RAM / integrated-GPU workstation.
3. Preserve verified work and avoid destructive changes.
4. Update `current report.md` after every meaningful development task.
5. Review outputs and test evidence before declaring a task complete.
6. Create commits directly on GitHub. Never create local commits on the user's computer.
7. Never push or publish unreviewed changes.

## Repository layout
- `current report.md` — durable project status and verification log.
- `projects/integration-smoke-test/` — first verified Blender production test.
- `docs/` — architecture and workflow documentation (to be developed).
- `agents/` — agent roles and orchestration (to be developed).
- `scripts/` — Blender and production automation (to be developed).
- `templates/` — reusable animation templates (to be developed).
- `assets/` — approved reusable assets (to be developed).
- `renders/` — preview and final outputs (to be developed).

## Getting started
Install Blender 5.3 or a compatible supported release, configure BlendRelay MCP for your agent environment, and open the `.blend` smoke-test project in Blender. Detailed setup and production workflow documentation will be added as the studio foundation is implemented.

## Current constraints
The initial workstation has an AMD Ryzen 5 5500U, 7.3 GB usable RAM, and integrated AMD Radeon graphics. Begin with Eevee, modest geometry, low texture sizes, and reduced-resolution previews. Treat 1080×1920 at 30 fps as a final-output target, not a default preview setting.