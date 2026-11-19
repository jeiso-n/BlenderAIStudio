"""Headless render helper for pole_drift.blend (does not save the .blend).

    blender -b pole_drift.blend --python render_pole_drift.py -- stills OUTDIR 1 100 200
    blender -b pole_drift.blend --python render_pole_drift.py -- video      (renders //preview.mp4)
"""
import os
import sys
import time

import bpy

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
mode = args[0] if args else "video"
scene = bpy.context.scene
t0 = time.time()

if mode == "stills":
    outdir = args[1]
    os.makedirs(outdir, exist_ok=True)
    scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "PNG"
    for f in (int(a) for a in args[2:]):
        scene.frame_set(f)
        scene.render.filepath = os.path.join(outdir, "frame_%04d.png" % f)
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
print("RENDER_DONE mode=%s seconds=%.1f" % (mode, time.time() - t0))
