# Production Notes — Integration Smoke Test

Built through BlendRelay MCP (`execute_blender_python`) in a live Blender 5.3.0 session; rendered with Blender background (CLI) using Eevee.

## Scene
- Dark studio with glossy floor, backdrop wall, metallic pedestal, and dark navy world.
- Hero: metallic icosahedron (`HeroIcosahedron`) with emissive pink torus ring (`HeroRing`).
- Title: 3D text `Title_BLENDER_AI_STUDIO` on two lines: “BLENDER AI” / “STUDIO”.
- Three area lights: warm key, cyan rim, and magenta fill.
- Active camera: `Camera`, 38 mm, portrait framing and track-to target.

## Animation
- Frames 1–120 at 24 fps (5 seconds).
- Hero rotates 360° around Z and gently hovers.
- Ring counter-rotates 360° and gently hovers.
- Title scales in and rises over frames 1–36 with eased interpolation.
- Keyframes were read back from Blender and confirmed.

## Render settings
- Eevee (`BLENDER_EEVEE`), 24 samples, 540×960, 24 fps.
- Video: FFmpeg container, H.264, medium quality.
- Preview: frame 60, saved as `preview.png`.
- Animation: 120 frames, rendered in approximately 300 seconds.

## Verified outputs
- `integration_smoke_test.blend` — editable Blender project.
- `preview.png` — 540×960 rendered still.
- `animation.mp4` — H.264, 540×960, 24 fps, 120 frames, 5.000 seconds (independently checked with FFprobe).
- `production_notes.md` — this document.

## Limitations
- Low resolution and sample count selected for an 8 GB-class RAM, integrated-GPU workstation.
- No motion blur; title has scale/rise animation but no fade.
- Animation rendered with Blender CLI from the saved project, not through the GUI render operator.
- The default Blender startup file was not overwritten; the open GUI document was replaced with this test scene.

## Integration result
PASS. Antigravity successfully connected to Blender 5.3.0 through BlendRelay MCP 0.7.8 and performed a read-only scene inspection. It then created the scene, materials, lighting, camera, keyframes, saved the project, and rendered outputs.