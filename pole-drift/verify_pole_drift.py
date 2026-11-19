"""Headless verification of pole_drift.blend.

    blender -b pole_drift.blend --python verify_pole_drift.py
Reads the saved file (no changes are saved) and prints PASS/FAIL facts.
"""
import math

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

scene = bpy.context.scene
ok = True


def check(label, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + label, detail)


def fcurves_of(o):
    ad = o.animation_data
    if not ad or not ad.action:
        return []
    try:
        return list(ad.action.fcurves)
    except AttributeError:
        return list(ad.action.layers[0].strips[0].channelbag(ad.action_slot).fcurves)


r = scene.render
check("engine Eevee", r.engine == "BLENDER_EEVEE", r.engine)
check("frame range 1-360", (scene.frame_start, scene.frame_end) == (1, 360), (scene.frame_start, scene.frame_end))
check("fps 24", r.fps == 24 and r.fps_base == 1.0, r.fps)
check("preview 640x360", (r.resolution_x, r.resolution_y, r.resolution_percentage) == (640, 360, 100))
check("8 samples", scene.eevee.taa_render_samples == 8, scene.eevee.taa_render_samples)
check("no motion blur", not r.use_motion_blur)
check("H.264 MP4", r.image_settings.file_format == "FFMPEG" and r.ffmpeg.codec == "H264", (r.ffmpeg.format, r.ffmpeg.codec))
check("active camera", scene.camera and scene.camera.name == "Camera", scene.camera.name if scene.camera else None)
lights = [o for o in scene.objects if o.type == "LIGHT"]
check("limited lights (<=5)", len(lights) <= 5, [o.name for o in lights])

for name in ("Car_Root", "Car_Chassis", "WheelPivot_FL", "WheelPivot_FR", "WheelSpin_FL",
             "WheelSpin_FR", "WheelSpin_RL", "WheelSpin_RR", "CamRig"):
    fcs = fcurves_of(bpy.data.objects[name])
    n = sum(len(fc.keyframe_points) for fc in fcs)
    check("keyframes on " + name, n >= 2, "%d fcurves, %d keys" % (len(fcs), n))
check("Build-modifier skid marks", all(any(m.type == "BUILD" for m in bpy.data.objects[n].modifiers)
                                         for n in ("SkidMark_RL", "SkidMark_RR")))

car = bpy.data.objects["Car_Root"]
body = bpy.data.objects["Car_Body"]
cam = scene.camera
corners = [Vector(c) for c in body.bound_box]

min_pole = 1e9
max_jump = 0.0
max_yaw_step = 0.0
prev = prev_yaw = None
vis_main, vis_all = [], []
max_z = 0.0
for f in range(1, 361):
    scene.frame_set(f)
    cw = car.matrix_world
    pos = cw.translation
    yaw = car.rotation_euler.z
    if prev is not None:
        max_jump = max(max_jump, (pos - prev).length)
        max_yaw_step = max(max_yaw_step, abs(yaw - prev_yaw))
    prev, prev_yaw = pos.copy(), yaw
    max_z = max(max_z, abs(pos.z))
    bw = [body.matrix_world @ c for c in corners]
    # footprint corners + edge midpoints against the pole (radius 0.38 base plate)
    pts = [Vector((p.x, p.y, 0)) for p in bw]
    for i in range(4):
        pts.append((pts[i] + pts[(i + 1) % 4]) / 2)
    min_pole = min(min_pole, min(math.hypot(p.x, p.y) for p in pts) - 0.38)
    # use the car-centre-relative nose (front-most of body) for clearance too
    nose = body.matrix_world @ Vector((0, 2.25, 0.4))
    min_pole = min(min_pole, math.hypot(nose.x, nose.y) - 0.38)
    # camera visibility of the car centre
    c = world_to_camera_view(scene, cam, Vector((pos.x, pos.y, 0.7)))
    inside = 0.0 <= c.x <= 1.0 and 0.0 <= c.y <= 1.0 and c.z > 0
    vis_all.append(inside)
    if 73 <= f <= 265:
        vis_main.append(inside)

check("car visible for all frames 73-265 (main drift)", all(vis_main), "%d/%d" % (sum(vis_main), len(vis_main)))
first_in = vis_all.index(True) + 1
last_in = len(vis_all) - vis_all[::-1].index(True)
check("car enters the frame after frame 1 (off-screen start)", first_in > 1, "first in-frame frame %d" % first_in)
print("INFO car centre in frame until frame %d (receding into the distance on exit)" % last_in)
check("no position jump (max step < 0.5 m)", max_jump < 0.5, "%.3f m/frame (expected %.3f)" % (max_jump, 9.74 / 24))
check("no yaw jump (max step < 10 deg)", math.degrees(max_yaw_step) < 10, "%.2f deg/frame" % math.degrees(max_yaw_step))
check("pole clearance > 2 m", min_pole > 2.0, "%.2f m min car-to-pole gap" % min_pole)
check("car grounded (|z| < 1 cm)", max_z < 0.01, "%.4f" % max_z)

# drift angle: heading minus velocity direction during the main drift
errs = []
for f in range(100, 240):
    scene.frame_set(f)
    p0 = car.matrix_world.translation.copy()
    scene.frame_set(f + 1)
    p1 = car.matrix_world.translation.copy()
    vel = math.atan2(p1.y - p0.y, p1.x - p0.x)
    head = car.rotation_euler.z + math.pi / 2          # forward is local +Y
    d = math.degrees((head - vel + math.pi) % (2 * math.pi) - math.pi)
    errs.append(d)
check("sustained drift (slip angle 25-45 deg)", 25 < min(errs) and max(errs) < 45,
      "slip min %.1f max %.1f deg" % (min(errs), max(errs)))

# wheel spin direction and steering
scene.frame_set(120)
a = bpy.data.objects["WheelSpin_FL"].rotation_euler.x
scene.frame_set(121)
b = bpy.data.objects["WheelSpin_FL"].rotation_euler.x
check("wheels roll forward (spin decreasing about +X)", b < a, "%.2f -> %.2f rad" % (a, b))
scene.frame_set(150)
st = math.degrees(bpy.data.objects["WheelPivot_FL"].rotation_euler.z)
check("front wheels steered during drift", abs(st) > 10, "%.1f deg" % st)

scene.frame_set(360)
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for o in scene.objects:
    if o.type == "MESH":
        eo = o.evaluated_get(dg)
        me = eo.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        eo.to_mesh_clear()
check("triangles < 20000", tris < 20000, tris)
print("OVERALL", "PASS" if ok else "FAIL")
