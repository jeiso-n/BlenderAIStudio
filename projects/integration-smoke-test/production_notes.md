# Production Notes — Integration Smoke Test

Built through BlendRelay MCP (`execute_blender_python`) in a live Blender 5.3.0 session; rendered with Blender background (CLI) Eevee.

## Scene
- Studio: dark floor (glossy), backdrop wall, metallic pedestal, dark navy world.
- Hero: metallic icosahedron (`HeroIcosahedron`) + emissive pink torus ring (`HeroRing`) at pedestal.
- Title: 3D text `Title_BLENDER_AI_STUDIO` ("BLENDER AI" / "STUDIO", two lines for vertical fit), emissive material.
- Lights: 3 area lights - warm key, cyan rim, magenta fill (track-to constraints on the hero).
- Camera: `Camera`, 38 mm, track-to on `LookTarget`, portrait framing.

## Animation (frames 1-120, 24 fps = 5 s)
- Hero: Z rotation 0->360 deg, LINEAR (seamless loop); gentle hover (Bezier, 3 keys).
- Ring: Z rotation 0->-360 deg, LINEAR; same hover.
- Title: scale 0.01->1 and rise 3.9->4.5 over frames 1-36, Bezier ease.

## Render settings
- Eevee (`BLENDER_EEVEE`), 24 TAA samples, 540x960, 24 fps.
- Video: FFmpeg MPEG-4 container, H.264, medium quality. (Blender 5.x: set `image_settings.media_type='VIDEO'` before `file_format='FFMPEG'`.)
- Preview: frame 60 -> `preview.png` (~5 s). Animation: 120 frames in ~300 s wall-clock.

## Limitations
- Low resolution/samples chosen for the 8 GB, integrated-GPU machine; no motion blur, no textures.
- Title appears with scale/rise only (no fade).
- Animation rendered via Blender CLI of the saved file, not inside the GUI session. The session's open document is now this project; the default startup file was not touched.
