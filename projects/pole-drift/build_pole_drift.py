"""Pole Drift - deterministic, rerunnable Blender build script.

Usage (headless, does not touch any other .blend):
    blender -b --factory-startup --python build_pole_drift.py

Builds the whole scene from scratch (low-poly sports car, night drift pad,
illuminated pole, skid marks, smoke puffs, lights, camera, keyframes, render
settings) and saves ./pole_drift.blend next to this script.
All motion is computed from closed-form functions of time (no randomness except
a fixed-seed generator for smoke-puff size), so every run is identical.
"""
import math
import os
import random

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_BLEND = os.path.join(HERE, "pole_drift.blend")

# ----------------------------------------------------------------- constants
FPS = 24
F_START, F_END = 1, 360            # 360 frames = exactly 15 s at 24 fps
R = 6.2                            # drift radius of the car centre (m)
OMEGA = math.pi / 2                # 90 deg/s around the pole -> 2 laps in 8 s
V = OMEGA * R                      # constant ground speed (m/s)
T_IN = 3.0                         # drift starts / circle joined
PHI_START = -math.pi / 2           # entry point (0,-R), heading +X
SWEEP = math.radians(720 + 128)    # two laps + arc that aims the exit away from camera
T_ARC_END = T_IN + SWEEP / OMEGA   # ~12.42 s
PHI_END = PHI_START + SWEEP
DRIFT_ANGLE = math.radians(36)     # nose points toward the pole
WHEEL_R = 0.36
POLE_H = 6.5
WHEEL_X, WHEEL_YF, WHEEL_YR = 1.0, 1.38, -1.32


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


# ----------------------------------------------------------- motion model
def car_state(t):
    """Closed-form car pose at time t (seconds). Pure function."""
    if t < T_IN:                                   # approach, straight line y=-R
        x, y, phi = V * (t - T_IN), -R, PHI_START
    elif t <= T_ARC_END:                           # circular drift around the pole
        phi = PHI_START + OMEGA * (t - T_IN)
        x, y = R * math.cos(phi), R * math.sin(phi)
    else:                                          # straight exit on the tangent
        phi = PHI_END
        ex, ey = R * math.cos(phi), R * math.sin(phi)
        tx, ty = -math.sin(phi), math.cos(phi)
        x, y = ex + tx * V * (t - T_ARC_END), ey + ty * V * (t - T_ARC_END)
    drift = smooth((t - 2.2) / 1.6) * (1.0 - smooth((t - 11.8) / 1.8))
    wob = math.sin(2 * math.pi * t / 1.9)
    alpha = DRIFT_ANGLE * drift + math.radians(1.8) * wob * drift
    yaw = phi + alpha
    turn_in = math.radians(12) * math.sin(math.pi * max(0.0, min(1.0, (t - 1.9) / 1.1)))
    steer = -0.85 * alpha + turn_in                # counter-steer once sliding
    roll = math.radians(3.0) * drift + math.radians(0.35) * math.sin(2 * math.pi * 1.1 * t) * drift
    pitch = math.radians(0.8) * drift + math.radians(0.3) * math.sin(2 * math.pi * 1.7 * t + 1.0) * drift
    bounce = 0.012 * math.sin(2 * math.pi * 2.3 * t) * drift
    return dict(x=x, y=y, phi=phi, yaw=yaw, alpha=alpha, steer=steer, drift=drift,
                roll=roll, pitch=pitch, bounce=bounce,
                spin_f=-V * t / WHEEL_R, spin_r=-1.1 * V * t / WHEEL_R)


def wheel_world(t, lx, ly):
    st = car_state(t)
    c, s = math.cos(st["yaw"]), math.sin(st["yaw"])
    return st["x"] + lx * c - ly * s, st["y"] + lx * s + ly * c


def frame_to_t(f):
    return (f - 1) / FPS


# ------------------------------------------------------------ scene reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "PoleDrift"
scene.frame_start, scene.frame_end = F_START, F_END
scene.render.fps, scene.render.fps_base = FPS, 1.0

colls = {}
for cname in ("Car", "Environment", "FX", "Lighting_Camera"):
    colls[cname] = bpy.data.collections.new(cname)
    scene.collection.children.link(colls[cname])


def link(o, cname):
    colls[cname].objects.link(o)
    return o


def empty(name, cname, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None)
    o.empty_display_size = 0.3
    o.location = loc
    o.parent = parent
    return link(o, cname)


def make_mat(name, color, metallic=0.0, rough=0.5, emit=None, strength=0.0,
             alpha=1.0, blended=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1.0)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    if emit is not None:
        b.inputs["Emission Color"].default_value = (*emit, 1.0)
        b.inputs["Emission Strength"].default_value = strength
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
    if blended:
        try:
            m.surface_render_method = "BLENDED"
        except Exception as e:  # older/newer API
            print("WARN blended:", e)
    return m


# --------------------------------------------------------- mesh builder
class MB:
    """Tiny mesh accumulator (vertices, faces, per-face material index)."""

    def __init__(self):
        self.v, self.f, self.m = [], [], []

    def add(self, verts, faces, mat=0):
        o = len(self.v)
        self.v += [tuple(p) for p in verts]
        self.f += [tuple(i + o for i in fc) for fc in faces]
        self.m += [mat] * len(faces)

    def box(self, c, size, mat=0):
        cx, cy, cz = c
        sx, sy, sz = (s / 2 for s in size)
        v = [(cx - sx, cy - sy, cz - sz), (cx + sx, cy - sy, cz - sz),
             (cx + sx, cy + sy, cz - sz), (cx - sx, cy + sy, cz - sz),
             (cx - sx, cy - sy, cz + sz), (cx + sx, cy - sy, cz + sz),
             (cx + sx, cy + sy, cz + sz), (cx - sx, cy + sy, cz + sz)]
        f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (3, 0, 4, 7), (1, 2, 6, 5)]
        self.add(v, f, mat)

    def loft(self, rings, mat=0):
        """rings: [(y, half_width, z_bottom, z_top)] along +Y -> closed tapered box."""
        base = len(self.v)
        verts = []
        for y, hw, zb, zt in rings:
            verts += [(-hw, y, zb), (hw, y, zb), (hw, y, zt), (-hw, y, zt)]
        faces = []
        for i in range(len(rings) - 1):
            a, b = i * 4, (i + 1) * 4
            for k in range(4):
                k2 = (k + 1) % 4
                faces.append((a + k, b + k, b + k2, a + k2))
        faces.append((0, 1, 2, 3))
        last = (len(rings) - 1) * 4
        faces.append((last + 3, last + 2, last + 1, last))
        self.add(verts, faces, mat)

    def prism_x(self, c, radius, x0, x1, n, mat=0, phase=0.0):
        """Cylinder whose axis is the X axis, centred at c=(cx,cy,cz)."""
        cx, cy, cz = c
        verts = []
        for x in (x0, x1):
            for i in range(n):
                a = phase + 2 * math.pi * i / n
                verts.append((cx + x, cy + radius * math.cos(a), cz + radius * math.sin(a)))
        faces = [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)]
        faces.append(tuple(reversed(range(n))))
        faces.append(tuple(range(n, 2 * n)))
        self.add(verts, faces, mat)

    def prism_z(self, c, radius, z0, z1, n, mat=0):
        cx, cy, cz = c
        verts = []
        for z in (z0, z1):
            for i in range(n):
                a = 2 * math.pi * i / n
                verts.append((cx + radius * math.cos(a), cy + radius * math.sin(a), z))
        faces = [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)]
        faces.append(tuple(reversed(range(n))))
        faces.append(tuple(range(n, 2 * n)))
        self.add(verts, faces, mat)

    def cone_z(self, c, radius, z0, z_apex, n, mat=0, cap=True):
        cx, cy, cz = c
        verts = [(cx + radius * math.cos(2 * math.pi * i / n),
                  cy + radius * math.sin(2 * math.pi * i / n), z0) for i in range(n)]
        verts.append((cx, cy, z_apex))
        faces = [(i, (i + 1) % n, n) for i in range(n)]
        if cap:
            faces.append(tuple(reversed(range(n))))
        self.add(verts, faces, mat)

    def to_mesh(self, name, mats, smooth_shading=False):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.v, [], self.f)
        me.update()
        for m in mats:
            me.materials.append(m)
        for p, mi in zip(me.polygons, self.m):
            p.material_index = mi
            p.use_smooth = smooth_shading
        return me


def mesh_obj(name, me, cname, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    o = bpy.data.objects.new(name, me)
    o.location, o.rotation_euler, o.parent = loc, rot, parent
    return link(o, cname)


def no_shadow(o):
    try:
        o.visible_shadow = False
    except Exception as e:
        print("WARN visible_shadow:", e)


# --------------------------------------------------------------- materials
M_BODY = make_mat("CarBody_Orange", (1.0, 0.2, 0.02), 0.2, 0.4, (1.0, 0.18, 0.02), 0.35)
M_GLASS = make_mat("CarGlass", (0.02, 0.04, 0.08), 0.7, 0.08)
M_TRIM = make_mat("CarTrim_Black", (0.02, 0.02, 0.025), 0.2, 0.5)
M_HEAD = make_mat("Headlight", (1, 1, 1), 0.0, 0.2, (1.0, 0.92, 0.75), 12.0)
M_TAIL = make_mat("Taillight", (0.5, 0.0, 0.0), 0.0, 0.3, (1.0, 0.03, 0.02), 10.0)
M_TIRE = make_mat("Tire", (0.015, 0.015, 0.018), 0.0, 0.8)
M_HUB = make_mat("Hub", (0.75, 0.78, 0.85), 0.9, 0.25)
M_MARK = make_mat("WheelMarker", (1, 1, 1), 0.0, 0.3, (0.2, 0.9, 1.0), 6.0)
M_ASPHALT = make_mat("Asphalt", (0.028, 0.03, 0.037), 0.0, 0.6)
M_PAD = make_mat("DriftPad", (0.045, 0.048, 0.058), 0.0, 0.42)
M_LINE = make_mat("RoadLine_White", (0.55, 0.57, 0.6), 0.0, 0.7)
M_YELLOW = make_mat("RoadLine_Yellow", (0.9, 0.65, 0.05), 0.0, 0.6)
M_SKID = make_mat("SkidMark", (0.006, 0.006, 0.008), 0.0, 0.9)
M_POLE = make_mat("Pole", (0.11, 0.115, 0.13), 0.7, 0.4)
M_LAMP = make_mat("LampPanel", (1, 1, 1), 0.0, 0.3, (1.0, 0.74, 0.38), 14.0)
M_BEAM = make_mat("LightBeam", (1, 0.8, 0.5), 0.0, 1.0, (1.0, 0.72, 0.35), 1.0,
                  alpha=0.02, blended=True)
M_BOLLARD = make_mat("Bollard", (0.05, 0.1, 0.12), 0.0, 0.5, (0.1, 0.85, 1.0), 5.0)
M_TREE = make_mat("TreeSilhouette", (0.012, 0.025, 0.035), 0.0, 1.0)
M_SMOKE = make_mat("TireSmoke", (0.8, 0.82, 0.86), 0.0, 1.0, (0.55, 0.57, 0.62), 0.5, alpha=0.4, blended=True)

# --------------------------------------------------------------- world
world = bpy.data.worlds.new("NightWorld")
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.015, 0.03, 0.075, 1.0)
bg.inputs["Strength"].default_value = 0.9
scene.world = world

# --------------------------------------------------------------- environment
mb = MB()
mb.add([(-80, -80, 0), (80, -80, 0), (80, 80, 0), (-80, 80, 0)], [(0, 1, 2, 3)])
mesh_obj("Ground", mb.to_mesh("Ground", [M_ASPHALT]), "Environment")

mb = MB()
mb.cone_z((0, 0, 0.004), 16.0, 0.004, 0.004, 64, cap=False)  # flat disc: fan with apex in plane
disc = mb.to_mesh("DriftPad", [M_PAD])
mesh_obj("DriftPad", disc, "Environment")

# restrained markings: dashed outer ring + solid yellow ring at the pole base
mb = MB()


def ring_arc(r0, r1, a0, a1, z, mat, steps=3):
    for k in range(steps):
        b0 = a0 + (a1 - a0) * k / steps
        b1 = a0 + (a1 - a0) * (k + 1) / steps
        v = [(r0 * math.cos(b0), r0 * math.sin(b0), z), (r1 * math.cos(b0), r1 * math.sin(b0), z),
             (r1 * math.cos(b1), r1 * math.sin(b1), z), (r0 * math.cos(b1), r0 * math.sin(b1), z)]
        mb.add(v, [(0, 3, 2, 1)], mat)


for i in range(36):
    a = 2 * math.pi * i / 36
    ring_arc(11.4, 11.65, a, a + math.radians(6), 0.008, 0)
mesh_obj("Markings_Dashed", mb.to_mesh("Markings_Dashed", [M_LINE]), "Environment")
mb = MB()
ring_arc(0.95, 1.2, 0, 2 * math.pi, 0.009, 0, steps=24)
mesh_obj("Markings_PoleRing", mb.to_mesh("Markings_PoleRing", [M_YELLOW]), "Environment")

# pole
mb = MB()
mb.prism_z((0, 0, 0), 0.38, 0.0, 0.14, 8, 0)
mb.prism_z((0, 0, 0), 0.11, 0.14, POLE_H, 8, 0)
mb.box((0, 0, POLE_H + 0.08), (1.0, 0.55, 0.16), 0)
pole_mesh = mb.to_mesh("Pole", [M_POLE])
mesh_obj("Pole", pole_mesh, "Environment")
mb = MB()
mb.prism_z((0, 0, 0), 0.125, 0.2, 0.45, 8, 0)
mb.prism_z((0, 0, 0), 0.125, 0.65, 0.9, 8, 0)
mesh_obj("Pole_Bands", mb.to_mesh("Pole_Bands", [M_YELLOW]), "Environment")
mb = MB()
mb.box((0, 0, POLE_H - 0.02), (0.88, 0.44, 0.04), 0)
mesh_obj("Pole_LampPanel", mb.to_mesh("Pole_LampPanel", [M_LAMP]), "Environment")
mb = MB()
mb.cone_z((0, 0, 0), 4.6, 0.02, POLE_H - 0.06, 20, 0, cap=False)
beam = mesh_obj("Pole_LightBeam", mb.to_mesh("Pole_LightBeam", [M_BEAM]), "Environment")
no_shadow(beam)

# boundary bollards (emissive meshes, not lights)
mb = MB()
for i in range(24):
    a = 2 * math.pi * i / 24 + math.radians(7.5)
    mb.box((15.5 * math.cos(a), 15.5 * math.sin(a), 0.28), (0.22, 0.22, 0.56), 0)
mesh_obj("Bollards", mb.to_mesh("Bollards", [M_BOLLARD]), "Environment")

# distant tree silhouettes
rng = random.Random(2024)
mb = MB()
for i in range(30):
    a = 2 * math.pi * i / 30 + rng.uniform(-0.05, 0.05)
    d = rng.uniform(44, 54)
    mb.cone_z((d * math.cos(a), d * math.sin(a), 0), rng.uniform(1.8, 2.8), 0.0,
              rng.uniform(5.0, 8.5), 8, 0)
mesh_obj("TreeLine", mb.to_mesh("TreeLine", [M_TREE]), "Environment")

# ------------------------------------------------------------------ car
car_root = empty("Car_Root", "Car")
car_body = empty("Car_Chassis", "Car", parent=car_root)

mb = MB()
mb.loft([(-2.2, 0.88, 0.38, 0.82), (-1.7, 1.0, 0.34, 0.90), (-0.2, 1.0, 0.34, 0.84),
         (1.2, 0.97, 0.34, 0.74), (2.25, 0.84, 0.36, 0.52)], 0)
# cabin (frustum): roof = body colour, rest = glass
cv = [(-0.9, -1.15, 0.74), (0.9, -1.15, 0.74), (0.9, 0.70, 0.74), (-0.9, 0.70, 0.74),
      (-0.66, -0.75, 1.24), (0.66, -0.75, 1.24), (0.66, 0.0, 1.24), (-0.66, 0.0, 1.24)]
base = len(mb.v)
mb.add(cv, [(4, 5, 6, 7)], 0)
mb.add(cv, [(0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (3, 0, 4, 7)], 1)
mb.box((0, -2.05, 1.12), (1.7, 0.4, 0.05), 2)               # spoiler wing
mb.box((-0.55, -2.0, 0.97), (0.06, 0.1, 0.28), 2)
mb.box((0.55, -2.0, 0.97), (0.06, 0.1, 0.28), 2)
mb.box((0, 2.15, 0.33), (1.5, 0.35, 0.04), 2)               # front splitter
for sx in (-1, 1):
    mb.box((sx * 0.55, 2.22, 0.47), (0.3, 0.12, 0.09), 3)   # headlights
    mb.box((sx * 0.62, -2.2, 0.76), (0.36, 0.1, 0.08), 4)   # tail lights
car_mesh = mb.to_mesh("CarBodyMesh", [M_BODY, M_GLASS, M_TRIM, M_HEAD, M_TAIL])
body_obj = mesh_obj("Car_Body", car_mesh, "Car", parent=car_body)
bev = body_obj.modifiers.new("Bevel", "BEVEL")
bev.width, bev.segments, bev.limit_method = 0.035, 1, "ANGLE"

wheel_defs = {"FL": (-WHEEL_X, WHEEL_YF), "FR": (WHEEL_X, WHEEL_YF),
              "RL": (-WHEEL_X, WHEEL_YR), "RR": (WHEEL_X, WHEEL_YR)}
pivots, spinners = {}, {}
for key, (wx, wy) in wheel_defs.items():
    pivot = empty("WheelPivot_" + key, "Car", (wx, wy, WHEEL_R), car_root)
    spin = empty("WheelSpin_" + key, "Car", (0, 0, 0), pivot)
    outward = 1.0 if wx > 0 else -1.0
    mb = MB()
    mb.prism_x((0, 0, 0), WHEEL_R, -0.14, 0.14, 12, 0)
    xo = 0.14 * outward
    mb.prism_x((0, 0, 0), 0.2, min(xo, xo + 0.02 * outward), max(xo, xo + 0.02 * outward), 6, 1)
    mb.box((xo + 0.03 * outward, 0, 0.28), (0.03, 0.08, 0.08), 2)   # asymmetric marker -> visible spin
    wm = mb.to_mesh("Wheel_" + key, [M_TIRE, M_HUB, M_MARK])
    mesh_obj("Wheel_" + key, wm, "Car", parent=spin)
    pivots[key], spinners[key] = pivot, spin

head = bpy.data.lights.new("Headlight_Spot", "SPOT")
head.energy, head.spot_size, head.spot_blend = 450, math.radians(75), 0.6
head.color = (1.0, 0.93, 0.8)
head.shadow_soft_size = 0.1
head.use_shadow = False
hl = bpy.data.objects.new("Headlight_Spot", head)
hl.parent, hl.location, hl.rotation_euler = car_root, (0, 2.0, 0.6), (math.radians(84), 0, 0)
link(hl, "Car")

# ------------------------------------------------------------ lights/camera
def track(o, target):
    c = o.constraints.new("TRACK_TO")
    c.target, c.track_axis, c.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"


tgt_cam = empty("CamTarget", "Lighting_Camera", (0, 0, 2.0))
tgt_light = empty("LightTarget", "Lighting_Camera", (0, 0, 1.0))

pole_l = bpy.data.lights.new("PoleLight", "POINT")
pole_l.energy, pole_l.color, pole_l.shadow_soft_size = 3000, (1.0, 0.72, 0.4), 0.25
pole_l.use_shadow = True
pl = bpy.data.objects.new("PoleLight", pole_l)
pl.location = (0, 0, POLE_H - 0.3)
link(pl, "Lighting_Camera")

for name, loc, energy, col, size in (("Rim_Cyan", (-13, 13, 8), 2200, (0.2, 0.85, 1.0), 6),
                                     ("Fill_Blue", (16, 14, 5), 900, (0.25, 0.4, 1.0), 6)):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy, ld.color, ld.size = energy, col, size
    ld.use_shadow = False
    lo = bpy.data.objects.new(name, ld)
    lo.location = loc
    link(lo, "Lighting_Camera")
    track(lo, tgt_light)

cam_data = bpy.data.cameras.new("Camera")
cam_data.lens, cam_data.clip_start, cam_data.clip_end = 28, 1.0, 300
cam_rig = empty("CamRig", "Lighting_Camera")
cam = bpy.data.objects.new("Camera", cam_data)
az, dist, height = math.radians(-52), 18.0, 8.0
cam.location = (dist * math.cos(az), dist * math.sin(az), height)
cam.parent = cam_rig
link(cam, "Lighting_Camera")
track(cam, tgt_cam)
scene.camera = cam

# ----------------------------------------------------------- skid marks
def skid_ribbon(name, lx, ly, f0, f1, width=0.2):
    pts = []
    for f in range(f0, f1 + 1):
        pts.append(wheel_world(frame_to_t(f), lx, ly))
    verts, faces = [], []
    n = len(pts)
    for i, (px, py) in enumerate(pts):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        tx, ty = bx - ax, by - ay
        ln = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / ln, tx / ln
        verts.append((px + nx * width / 2, py + ny * width / 2, 0.012))
        verts.append((px - nx * width / 2, py - ny * width / 2, 0.012))
    for i in range(n - 1):
        a = 2 * i
        faces.append((a, a + 1, a + 3, a + 2))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    me.materials.append(M_SKID)
    o = mesh_obj(name, me, "FX")
    no_shadow(o)
    mod = o.modifiers.new("Reveal", "BUILD")        # faces appear chronologically
    mod.frame_start, mod.frame_duration = f0, f1 - f0
    return o


SK0, SK1 = 61, 322        # marks begin as the slide starts, end as the car straightens
skid_ribbon("SkidMark_RL", -WHEEL_X, WHEEL_YR, SK0, SK1)
skid_ribbon("SkidMark_RR", WHEEL_X, WHEEL_YR, SK0, SK1)

# ------------------------------------------------------------ smoke puffs
ico_t = (1 + math.sqrt(5)) / 2
ico_v = [(-1, ico_t, 0), (1, ico_t, 0), (-1, -ico_t, 0), (1, -ico_t, 0), (0, -1, ico_t),
         (0, 1, ico_t), (0, -1, -ico_t), (0, 1, -ico_t), (ico_t, 0, -1), (ico_t, 0, 1),
         (-ico_t, 0, -1), (-ico_t, 0, 1)]
ico_v = [tuple(0.5 * c / math.sqrt(1 + ico_t ** 2) for c in v) for v in ico_v]
ico_f = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4),
         (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),
         (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
mb = MB()
mb.add(ico_v, ico_f)
puff_mesh = mb.to_mesh("PuffMesh", [M_SMOKE])
rng = random.Random(1234)
PUFF_LIFE = 28
puffs = []
pf_start = int(round(3.0 * FPS)) + 1
pf_end = int(round(12.8 * FPS)) + 1
for idx, f in enumerate(range(pf_start, pf_end, 2)):
    key = "RL" if idx % 2 == 0 else "RR"
    wx, wy = wheel_defs[key]
    px, py = wheel_world(frame_to_t(f), wx, wy)
    o = mesh_obj("Puff_%03d" % idx, puff_mesh, "FX")
    no_shadow(o)
    o.rotation_euler = (rng.uniform(0, 3), rng.uniform(0, 3), rng.uniform(0, 3))
    smax = rng.uniform(0.9, 1.5)
    rl = math.hypot(px, py) or 1.0
    ox, oy = px / rl * 0.9, py / rl * 0.9
    puffs.append((o, f, px, py, ox, oy, smax))

# ------------------------------------------------------------- animation
def key(o, path, idx, frame, value):
    cur = getattr(o, path)
    if idx is None:
        setattr(o, path, value)
        o.keyframe_insert(path, frame=frame)
    else:
        cur[idx] = value
        o.keyframe_insert(path, index=idx, frame=frame)


car_root.rotation_mode = "XYZ"
for f in range(F_START, F_END + 1):
    t = frame_to_t(f)
    st = car_state(t)
    key(car_root, "location", 0, f, st["x"])
    key(car_root, "location", 1, f, st["y"])
    key(car_root, "rotation_euler", 2, f, st["yaw"])
    key(car_body, "rotation_euler", 0, f, st["pitch"])
    key(car_body, "rotation_euler", 1, f, st["roll"])
    key(car_body, "location", 2, f, st["bounce"])
    for k in ("FL", "FR"):
        key(pivots[k], "rotation_euler", 2, f, st["steer"])
        key(spinners[k], "rotation_euler", 0, f, st["spin_f"])
    for k in ("RL", "RR"):
        key(spinners[k], "rotation_euler", 0, f, st["spin_r"])

for o, f, px, py, ox, oy, smax in puffs:
    d = f + PUFF_LIFE
    o.location = (px, py, 0.3)
    o.keyframe_insert("location", frame=f - 1)
    o.location = (px + ox, py + oy, 1.5)
    o.keyframe_insert("location", frame=d)
    for fr, s in ((f - 1, 0.0), (f + 7, smax), (d, 0.0)):
        o.scale = (s, s, s)
        o.keyframe_insert("scale", frame=fr)

# restrained camera orbit (22 deg over the whole shot, eased)
cam_rig.rotation_euler = (0, 0, 0)
cam_rig.keyframe_insert("rotation_euler", index=2, frame=F_START)
cam_rig.rotation_euler = (0, 0, math.radians(22))
cam_rig.keyframe_insert("rotation_euler", index=2, frame=F_END)


def fcurves_of(o):
    ad = o.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    try:
        return list(act.fcurves)
    except AttributeError:        # Blender 5.x slotted/layered actions
        return list(act.layers[0].strips[0].channelbag(ad.action_slot).fcurves)


for o in [car_root, car_body] + list(pivots.values()) + list(spinners.values()):
    for fc in fcurves_of(o):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
for o, *_ in puffs:
    for fc in fcurves_of(o):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR" if fc.data_path == "location" else "BEZIER"

# ------------------------------------------------------- render settings
r = scene.render
r.engine = "BLENDER_EEVEE"
r.resolution_x, r.resolution_y, r.resolution_percentage = 640, 360, 100
r.use_motion_blur = False
ee = scene.eevee
for attr, val in (("taa_render_samples", 8), ("taa_samples", 8), ("use_shadows", True),
                  ("shadow_ray_count", 1), ("shadow_step_count", 4), ("use_raytracing", False),
                  ("use_volumetric_shadows", False)):
    if hasattr(ee, attr):
        setattr(ee, attr, val)
try:
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
except Exception as e:
    print("WARN color management:", e)
im = r.image_settings
im.media_type = "VIDEO"
im.file_format = "FFMPEG"
r.ffmpeg.format, r.ffmpeg.codec = "MPEG4", "H264"
r.ffmpeg.constant_rate_factor, r.ffmpeg.ffmpeg_preset = "MEDIUM", "GOOD"
r.filepath = "//preview.mp4"

scene.frame_set(150)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)

# ------------------------------------------------------------- stats
scene.frame_set(F_END)
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for o in scene.objects:
    if o.type == "MESH":
        eo = o.evaluated_get(dg)
        me = eo.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        eo.to_mesh_clear()
print("POLE_DRIFT_BUILD_OK objects=%d triangles=%d puffs=%d saved=%s"
      % (len(scene.objects), tris, len(puffs), OUT_BLEND))
