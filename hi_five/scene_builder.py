from __future__ import annotations

import json
import os
import bpy

from .node_arrange import arrange_nodes

# ──────────────────────────────────────────────
# Naming convention
# ──────────────────────────────────────────────
PREFIX = "_CNC_"
COLLECTION_NAME = "_CNC_Toolkit"
WORLD_NAME = f"{PREFIX}World"
COMP_TREE_NAME = f"{PREFIX}Composition"
ALPHA_CONVERT_NAME = f"{PREFIX}Alpha Convert"
ENGINE_MAP = {"CYCLES": "CYCLES", "EEVEE": "BLENDER_EEVEE"}

# ──────────────────────────────────────────────
# HDRI asset paths
# ──────────────────────────────────────────────
ADDON_DIR = os.path.dirname(os.path.realpath(__file__))
ASSET_DIR = os.path.join(ADDON_DIR, "assets")
GENERIC_HDRI = os.path.join(ASSET_DIR, "generic_hdri.exr")
DESOLATED_HDRI = os.path.join(ASSET_DIR, "desolated_hdri.exr")


# ──────────────────────────────────────────────
# Game configs
# ──────────────────────────────────────────────
class GameConfig:
  resolution = (640, 480)
  camera_type = "ORTHO"
  camera_location = (110.039, -110.039, 89.84670)
  camera_rotation = (1.0472, 0, 0.785398)
  camera_ortho_scale = 29.92
  camera_clip_end = 2000.0
  camera_iso_location = (0, -31.96573, 26.8228)
  camera_iso_rotation = (0.872665, 0, 0)
  camera_iso_ortho_scale = 53.37
  sun_location = (-4.14, -10, 12.27)
  sun_rotation = (0.633555, 0.0726057, 5.79449)
  sun_energy = 7.5
  sun_angle = 0.00392699
  hdri = GENERIC_HDRI
  cycles_samples = 64
  cycles_adaptive_min_samples = 32
  cycles_preview_samples = 10
  cycles_max_bounces = 4
  cycles_filter_width = 0.9
  colorramp_position01 = 0.717273
  colorramp_position02 = 0.722727
  colorramp_color01 = (0, 0, 1, 0)
  colorramp_color02 = (0, 0, 0.250158, 1)
  sky_sun_elevation = 0.933751
  sky_sun_rotation = 3.54302


def _make_config():
  return GameConfig()


GAME_CONFIGS = {}

for game_key, overrides in {
  "RA2": {
    "INF": {"resolution": (320, 240), "camera_ortho_scale": 14.96, "sun_location": (0, 0, 12.27), "sun_rotation": (0, 0, 0)},
  },
  "TS": {
    "BASE": {"camera_ortho_scale": 37.4, "sun_location": (-0.800477, -10.1766, 12.27), "sun_rotation": (0.633555, 0.0726057, 6.10865), "sun_energy": 5},
    "INF": {"resolution": (320, 240), "camera_ortho_scale": 18.7},
  },
  "RW": {
    "BASE": {"resolution": (1280, 960), "camera_ortho_scale": 37.4, "sun_location": (-0.800477, -10.1766, 12.27), "sun_rotation": (0.633555, 0.0726057, 6.10865), "sun_energy": 7.5},
  },
  "RA1": {
    "BASE": {"camera_type": "PERSP", "camera_location": (0, -36.2837, 30.4457), "camera_rotation": (0.872665, 0, 0), "camera_ortho_scale": 1.0472, "camera_iso_location": (0, -31.96573, 26.8228), "camera_iso_rotation": (0.872665, 0, 0), "camera_iso_ortho_scale": 53.37, "sun_location": (-4.0, 4.0, 16.0), "sun_rotation": (-0.10472, -0.179769, 0.00762709), "sun_energy": 6.5, "sky_sun_elevation": 1.37881, "sky_sun_rotation": 5.29184},
  },
  "RM": {
    "BASE": {"camera_type": "PERSP", "camera_location": (0, -36.2837, 30.4457), "camera_rotation": (0.872665, 0, 0), "camera_ortho_scale": 20.0138, "camera_iso_location": (0, -31.9657, 26.8228), "camera_iso_rotation": (0.872665, 0, 0), "camera_iso_ortho_scale": 20.0138, "sun_location": (-4.0, 4.0, 16.0), "sun_rotation": (-0.10472, -0.179769, 0.00762709), "sun_energy": 6.5, "sky_sun_elevation": 1.37881, "sky_sun_rotation": 5.29184},
  },
  "D2K": {
    "BASE": {"camera_type": "PERSP", "camera_location": (0, -28.3854, 23.8179), "camera_rotation": (0.872665, 0, 0), "camera_ortho_scale": 39.4299, "camera_iso_location": (0, -37.8463, 31.7564), "camera_iso_rotation": (0.872665, 0, 0), "camera_iso_ortho_scale": 39.4299, "sun_location": (-4.0, 4.0, 16.0), "sun_rotation": (-0.698132, 0, 2.35619), "sun_energy": 6.5, "sky_sun_elevation": 0.884882, "sky_sun_rotation": 3.92874},
  },
}.items():
  base = _make_config()
  for k, v in overrides.get("BASE", {}).items():
    setattr(base, k, v)
  GAME_CONFIGS[game_key] = {"BASE": base}
  for variant in ("INF", "FX"):
    if variant in overrides:
      cfg = _make_config()
      for attr in dir(base):
        if not attr.startswith("_"):
          setattr(cfg, attr, getattr(base, attr))
      for k, v in overrides[variant].items():
        setattr(cfg, k, v)
      GAME_CONFIGS[game_key][variant] = cfg
    else:
      GAME_CONFIGS[game_key][variant] = base


def get_config(game, variant):
  game_dict = GAME_CONFIGS.get(game)
  if not game_dict:
    return GAME_CONFIGS["RA2"]["BASE"]
  return game_dict.get(variant, game_dict["BASE"])


# ──────────────────────────────────────────────
# Snapshot / restore
# ──────────────────────────────────────────────
def save_scene_state(context):
  scene = context.scene
  state = {
    "resolution_x": scene.render.resolution_x,
    "resolution_y": scene.render.resolution_y,
    "engine": scene.render.engine,
    "fps": scene.render.fps,
    "film_transparent": scene.render.film_transparent,
    "color_mode": scene.render.image_settings.color_mode,
    "file_format": scene.render.image_settings.file_format,
    "frame_start": scene.frame_start,
    "frame_end": scene.frame_end,
    "world": scene.world.name if scene.world else "",
    "compositor": scene.compositing_node_group.name if scene.compositing_node_group else "",
    "filter_size": scene.render.filter_size,
    "filter_width": scene.cycles.filter_width if scene.render.engine == "CYCLES" else 0.0,
  }
  context.scene.cc_toolkit.saved_state = json.dumps(state)


def restore_scene_state(context):
  props = context.scene.cc_toolkit
  if not props.saved_state:
    return
  state = json.loads(props.saved_state)
  scene = context.scene
  scene.render.resolution_x = state["resolution_x"]
  scene.render.resolution_y = state["resolution_y"]
  scene.render.engine = state["engine"]
  scene.render.fps = state["fps"]
  scene.render.film_transparent = state["film_transparent"]
  scene.render.image_settings.color_mode = state["color_mode"]
  scene.render.image_settings.file_format = state["file_format"]
  scene.frame_start = state["frame_start"]
  scene.frame_end = state["frame_end"]
  if state["world"] and state["world"] in bpy.data.worlds:
    scene.world = bpy.data.worlds[state["world"]]
  if state["compositor"] and state["compositor"] in bpy.data.node_groups:
    scene.compositing_node_group = bpy.data.node_groups[state["compositor"]]
  scene.render.filter_size = state["filter_size"]
  if state["engine"] == "CYCLES":
    scene.cycles.filter_width = state["filter_width"]


# ──────────────────────────────────────────────
# Cleanup
# ──────────────────────────────────────────────
def clear_template(context):
  names_to_clean = []
  for name in bpy.data.collections.keys():
    if PREFIX in name or name == COLLECTION_NAME:
      names_to_clean.append(name)
  for name in names_to_clean:
    coll = bpy.data.collections.get(name)
    if coll:
      _delete_collection(coll)

  for block_type in ("materials", "worlds", "node_groups", "images"):
    data_block = getattr(bpy.data, block_type)
    to_remove = [k for k in data_block.keys() if k.startswith(PREFIX)]
    for name in to_remove:
      block = data_block.get(name)
      if block:
        data_block.remove(block)

  for obj in bpy.data.objects:
    if obj.name.startswith(PREFIX):
      bpy.data.objects.remove(obj, do_unlink=True)

  if context.scene.compositing_node_group and context.scene.compositing_node_group.name.startswith(PREFIX):
    context.scene.compositing_node_group = None


def _delete_collection(coll):
  for child in list(coll.children):
    _delete_collection(child)
  for obj in list(coll.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
  bpy.data.collections.remove(coll)


# ──────────────────────────────────────────────
# Rebuild
# ──────────────────────────────────────────────
def rebuild_all(context):
  props = context.scene.cc_toolkit
  scene = context.scene
  saved_compositing = scene.render.use_compositing
  scene.render.use_compositing = False
  target_engine = ENGINE_MAP[props.engine]
  if scene.render.engine != target_engine:
    scene.render.engine = target_engine
  clear_template(context)

  vl = context.view_layer
  if props.remap_materials:
    vl.use_pass_cryptomatte_material = True
    vl.pass_cryptomatte_depth = max(vl.pass_cryptomatte_depth, 2)
  else:
    vl.use_pass_cryptomatte_material = False

  create_collections(context)
  create_camera(context, props)
  create_light(context, props)
  create_world(context, props)
  create_planes(context)
  create_compositor(context, props)

  arrange_nodes([tree for tree in bpy.data.node_groups if tree.name.startswith(PREFIX) or ALPHA_CONVERT_NAME in tree.name])

  apply_render_settings(context, props)
  apply_render_type_visibility(context)

  crop = context.scene.cc_crop_canvas
  if crop.use_crop_canvas:
    crop.update_resolution(context)

  scene.render.use_compositing = saved_compositing


# ──────────────────────────────────────────────
# Collections
# ──────────────────────────────────────────────
def create_collections(context):
  coll = bpy.data.collections.new(COLLECTION_NAME)
  context.scene.collection.children.link(coll)
  shadow_coll = bpy.data.collections.new(f"{COLLECTION_NAME} Shadow")
  coll.children.link(shadow_coll)
  holdout_coll = bpy.data.collections.new(f"{COLLECTION_NAME} Holdout")
  coll.children.link(holdout_coll)


# ──────────────────────────────────────────────
# Camera
# ──────────────────────────────────────────────
def create_camera(context, props):
  vll = context.view_layer.layer_collection
  context.view_layer.active_layer_collection = vll.children[COLLECTION_NAME]
  config = get_config(props.game, props.variant)

  if props.game in {"RA1", "RM", "D2K"} and props.camera_mode == "ORTHO":
    location = config.camera_iso_location
    rotation = config.camera_iso_rotation
    cam_type = "ORTHO"
    ortho_scale = config.camera_iso_ortho_scale
  else:
    location = config.camera_location
    rotation = config.camera_rotation
    cam_type = config.camera_type
    ortho_scale = config.camera_ortho_scale

  cam_data = bpy.data.cameras.new(f"{PREFIX}Camera")
  cam_obj = bpy.data.objects.new(f"{PREFIX}Camera", cam_data)
  bpy.data.collections[COLLECTION_NAME].objects.link(cam_obj)
  cam_obj.location = location
  cam_obj.rotation_euler = rotation
  cam_obj.hide_viewport = True
  cam_data.type = cam_type
  if cam_type == "PERSP":
    cam_data.lens_unit = "FOV"
    cam_data.angle = 1.0472
  else:
    cam_data.ortho_scale = ortho_scale
    cam_data.clip_end = config.camera_clip_end
  context.scene.camera = cam_obj
  _set_camera_view(context)


def _set_camera_view(context):
  for area in context.screen.areas:
    if area.type == "VIEW_3D":
      for space in area.spaces:
        if space.type == "VIEW_3D":
          space.region_3d.view_perspective = "CAMERA"
          return


# ──────────────────────────────────────────────
# Light
# ──────────────────────────────────────────────
def create_light(context, props):
  vll = context.view_layer.layer_collection
  context.view_layer.active_layer_collection = vll.children[COLLECTION_NAME]
  config = get_config(props.game, props.variant)
  bpy.ops.object.light_add(
    type="SUN", radius=1, align="WORLD",
    location=config.sun_location, rotation=config.sun_rotation,
  )
  sun = context.active_object
  sun.name = f"{PREFIX}Sun"
  sun.data.name = f"{PREFIX}Sun"
  sun.data.energy = config.sun_energy
  sun.data.angle = config.sun_angle
  sun.data.cycles.use_multiple_importance_sampling = False
  sun.hide_select = True
  sun.hide_render = True


# ──────────────────────────────────────────────
# World
# ──────────────────────────────────────────────
def create_world(context, props):
  config = get_config(props.game, props.variant)

  world = bpy.data.worlds.new(WORLD_NAME)
  context.scene.world = world
  world.color = (0, 0, 0)

  tree = world.node_tree
  out_cycles = tree.nodes["World Output"]
  out_cycles.target = "CYCLES"
  out_eevee = tree.nodes.new("ShaderNodeOutputWorld")
  out_eevee.target = "EEVEE"
  tree.links.remove(out_cycles.inputs[0].links[0])

  tex_coord = tree.nodes.new("ShaderNodeTexCoord")
  lightpath = tree.nodes.new("ShaderNodeLightPath")
  mapping1 = tree.nodes.new("ShaderNodeMapping")
  mapping1.inputs[1].default_value[2] = 0.3
  mapping2 = tree.nodes.new("ShaderNodeMapping")
  mapping2.inputs[2].default_value[2] = -1.5708

  data_image = bpy.data.images.get(os.path.basename(config.hdri))
  if not data_image:
    data_image = bpy.data.images.load(config.hdri)
  tex_env = tree.nodes.new("ShaderNodeTexEnvironment")
  tex_env.image = data_image
  tex_env.image.use_fake_user = True

  hs_sky = tree.nodes.new("ShaderNodeHueSaturation")
  hs_sky.inputs[0].default_value = 0.5
  hs_sky.inputs[1].default_value = 0.75
  hs_sky.inputs[2].default_value = 0.9
  hs_env = tree.nodes.new("ShaderNodeHueSaturation")
  hs_env.inputs[0].default_value = 0.5
  hs_env.inputs[1].default_value = 0.5
  hs_env.inputs[2].default_value = 0.6

  bg_cycles = tree.nodes["Background"]
  bg_sky = tree.nodes.new("ShaderNodeBackground")
  bg_sky.inputs[0].default_value = (1, 1, 1, 1)
  bg_blue = tree.nodes.new("ShaderNodeBackground")
  bg_blue.inputs[0].default_value = (0, 0, 1, 1)
  bg_eevee = tree.nodes.new("ShaderNodeBackground")
  bg_eevee.inputs[0].default_value = (0, 0.5, 0.5, 1)

  mix1 = tree.nodes.new("ShaderNodeMixShader")
  mix2 = tree.nodes.new("ShaderNodeMixShader")
  mix3 = tree.nodes.new("ShaderNodeMixShader")
  mix_rgb = tree.nodes.new("ShaderNodeMixRGB")
  mix_rgb.inputs[1].default_value = (0, 0, 0, 1)

  cr1 = tree.nodes.new("ShaderNodeValToRGB")
  cr1.color_ramp.elements[0].position = 0.25
  cr1.color_ramp.elements[1].position = 0.327273
  cr2 = tree.nodes.new("ShaderNodeValToRGB")
  cr2.color_ramp.interpolation = "EASE"
  cr2.color_ramp.elements[0].position = 0.5
  cr2.color_ramp.elements[1].position = 1.0

  sep_rgb = tree.nodes.new("ShaderNodeSeparateColor")
  sky = tree.nodes.new("ShaderNodeTexSky")
  sky.sun_size = 0
  sky.sun_intensity = 0.1
  sky.sun_elevation = config.sky_sun_elevation
  sky.sun_rotation = config.sky_sun_rotation
  sky.altitude = 20000
  sky.air_density = 1
  sky.aerosol_density = 0.05
  sky.ozone_density = 0.05
  sky.sky_type = "SINGLE_SCATTERING"

  noise = tree.nodes.new("ShaderNodeTexNoise")
  noise.inputs[2].default_value = 4
  noise.inputs[3].default_value = 5
  noise.inputs[5].default_value = 0.5

  tree.links.new(mix1.outputs[0], out_cycles.inputs[0])
  tree.links.new(lightpath.outputs[0], mix1.inputs[0])
  tree.links.new(mix2.outputs[0], mix1.inputs[1])
  tree.links.new(mix_rgb.outputs[0], mix2.inputs[0])
  tree.links.new(cr1.outputs[0], mix_rgb.inputs[0])
  tree.links.new(sep_rgb.outputs[2], cr1.inputs[0])
  tree.links.new(mapping1.outputs[0], sep_rgb.inputs[0])
  tree.links.new(tex_coord.outputs[0], mapping1.inputs[0])
  tree.links.new(bg_cycles.outputs[0], mix2.inputs[1])
  tree.links.new(hs_sky.outputs[0], bg_cycles.inputs[0])
  tree.links.new(sky.outputs[0], hs_sky.inputs[4])
  tree.links.new(bg_sky.outputs[0], mix2.inputs[2])
  tree.links.new(bg_blue.outputs[0], mix1.inputs[2])
  tree.links.new(cr2.outputs[0], mix_rgb.inputs[2])
  tree.links.new(noise.outputs[0], cr2.inputs[0])
  tree.links.new(mapping1.outputs[0], noise.inputs[0])

  tree.links.new(mix3.outputs[0], out_eevee.inputs[0])
  tree.links.new(lightpath.outputs[0], mix3.inputs[0])
  tree.links.new(bg_blue.outputs[0], mix3.inputs[2])
  tree.links.new(bg_eevee.outputs[0], mix3.inputs[1])
  tree.links.new(tex_env.outputs[0], hs_env.inputs[4])
  tree.links.new(hs_env.outputs[0], bg_eevee.inputs[0])
  tree.links.new(mapping2.outputs[0], tex_env.inputs[0])
  tree.links.new(tex_coord.outputs[0], mapping2.inputs[0])


# ──────────────────────────────────────────────
# Planes and materials
# ──────────────────────────────────────────────
def _make_plane(name, size=140, location=(0, 0, -0.01), hide_render=True, hide_viewport=True, glossy=False, shadow_catcher=False, material=None):
  bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=False, align="WORLD", location=location)
  obj = bpy.context.active_object
  obj.name = name
  obj.hide_render = hide_render
  obj.hide_viewport = hide_viewport
  obj.visible_glossy = glossy
  obj.is_shadow_catcher = shadow_catcher
  if material:
    obj.data.materials.append(material)
  return obj


def _ambient_mat():
  m = bpy.data.materials.new(name=f"{PREFIX}Plane.ambient")
  m.node_tree.nodes.remove(m.node_tree.nodes["Principled BSDF"])
  out = m.node_tree.nodes["Material Output"]
  lp = m.node_tree.nodes.new("ShaderNodeLightPath")
  d1 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d1.inputs[0].default_value = (0.0193824, 0.0193824, 0.0193824, 1)
  d2 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d2.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  tr = m.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  ho = m.node_tree.nodes.new("ShaderNodeHoldout")
  mx1, mx2, mx3 = (m.node_tree.nodes.new("ShaderNodeMixShader") for _ in range(3))
  m.node_tree.links.new(mx3.outputs[0], out.inputs[0])
  m.node_tree.links.new(ho.outputs[0], mx3.inputs[2])
  m.node_tree.links.new(mx2.outputs[0], mx3.inputs[1])
  m.node_tree.links.new(lp.outputs[0], mx3.inputs[0])
  m.node_tree.links.new(lp.outputs[3], mx2.inputs[0])
  m.node_tree.links.new(d1.outputs[0], mx2.inputs[1])
  m.node_tree.links.new(mx1.outputs[0], mx2.inputs[2])
  m.node_tree.links.new(d2.outputs[0], mx1.inputs[2])
  m.node_tree.links.new(tr.outputs[0], mx1.inputs[1])
  return m


def _blue_mat():
  m = bpy.data.materials.new(name=f"{PREFIX}Plane.blue")
  m.node_tree.nodes.remove(m.node_tree.nodes["Principled BSDF"])
  out = m.node_tree.nodes["Material Output"]
  lp = m.node_tree.nodes.new("ShaderNodeLightPath")
  d1 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d1.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  d2 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d2.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  d3 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d3.inputs[0].default_value = (0, 0, 1, 1)
  d3.inputs[1].default_value = 0
  tr = m.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  mx1, mx2, mx3 = (m.node_tree.nodes.new("ShaderNodeMixShader") for _ in range(3))
  m.node_tree.links.new(mx3.outputs[0], out.inputs[0])
  m.node_tree.links.new(d3.outputs[0], mx3.inputs[2])
  m.node_tree.links.new(mx2.outputs[0], mx3.inputs[1])
  m.node_tree.links.new(lp.outputs[0], mx3.inputs[0])
  m.node_tree.links.new(lp.outputs[3], mx2.inputs[0])
  m.node_tree.links.new(d1.outputs[0], mx2.inputs[1])
  m.node_tree.links.new(mx1.outputs[0], mx2.inputs[2])
  m.node_tree.links.new(d2.outputs[0], mx1.inputs[2])
  m.node_tree.links.new(tr.outputs[0], mx1.inputs[1])
  return m


def _grey_mat():
  m = bpy.data.materials.new(name=f"{PREFIX}Plane.grey")
  m.node_tree.nodes.remove(m.node_tree.nodes["Principled BSDF"])
  out = m.node_tree.nodes["Material Output"]
  lp = m.node_tree.nodes.new("ShaderNodeLightPath")
  d1 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d1.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  d2 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d2.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  tr = m.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  mx1, mx2 = (m.node_tree.nodes.new("ShaderNodeMixShader") for _ in range(2))
  m.node_tree.links.new(lp.outputs[3], mx2.inputs[0])
  m.node_tree.links.new(d1.outputs[0], mx2.inputs[1])
  m.node_tree.links.new(tr.outputs[0], mx1.inputs[1])
  m.node_tree.links.new(d2.outputs[0], mx1.inputs[2])
  m.node_tree.links.new(mx1.outputs[0], mx2.inputs[2])
  m.node_tree.links.new(mx2.outputs[0], out.inputs[0])
  return m


def _holdout_mat():
  m = bpy.data.materials.new(name=f"{PREFIX}Plane.holdout")
  m.node_tree.nodes.remove(m.node_tree.nodes["Principled BSDF"])
  out = m.node_tree.nodes["Material Output"]
  lp = m.node_tree.nodes.new("ShaderNodeLightPath")
  d1 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d1.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  d2 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d2.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  tr = m.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  ho = m.node_tree.nodes.new("ShaderNodeHoldout")
  mx1, mx2, mx3 = (m.node_tree.nodes.new("ShaderNodeMixShader") for _ in range(3))
  m.node_tree.links.new(tr.outputs[0], mx1.inputs[1])
  m.node_tree.links.new(d2.outputs[0], mx1.inputs[2])
  m.node_tree.links.new(mx1.outputs[0], mx2.inputs[2])
  m.node_tree.links.new(lp.outputs[3], mx2.inputs[0])
  m.node_tree.links.new(d1.outputs[0], mx2.inputs[1])
  m.node_tree.links.new(lp.outputs[0], mx3.inputs[0])
  m.node_tree.links.new(mx2.outputs[0], mx3.inputs[1])
  m.node_tree.links.new(ho.outputs[0], mx3.inputs[2])
  m.node_tree.links.new(mx3.outputs[0], out.inputs[0])
  return m


def _shadow_mat():
  m = bpy.data.materials.new(name=f"{PREFIX}Plane.shadow")
  m.node_tree.nodes.remove(m.node_tree.nodes["Principled BSDF"])
  out_c = m.node_tree.nodes["Material Output"]
  out_c.target = "CYCLES"
  lp = m.node_tree.nodes.new("ShaderNodeLightPath")
  d1 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d1.inputs[0].default_value = (0.090655, 0.090655, 0.090655, 1)
  d2 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d2.inputs[0].default_value = (0.401978, 0.401978, 0.401978, 1)
  tr = m.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  mx1, mx2 = (m.node_tree.nodes.new("ShaderNodeMixShader") for _ in range(2))
  m.node_tree.links.new(lp.outputs[3], mx2.inputs[0])
  m.node_tree.links.new(d1.outputs[0], mx2.inputs[1])
  m.node_tree.links.new(tr.outputs[0], mx1.inputs[1])
  m.node_tree.links.new(d2.outputs[0], mx1.inputs[2])
  m.node_tree.links.new(mx1.outputs[0], mx2.inputs[2])
  m.node_tree.links.new(mx2.outputs[0], out_c.inputs[0])
  out_e = m.node_tree.nodes.new("ShaderNodeOutputMaterial")
  out_e.target = "EEVEE"
  mx3 = m.node_tree.nodes.new("ShaderNodeMixShader")
  pbr = m.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
  pbr.inputs[0].default_value = (0.371235, 0.371238, 0.371238, 0)
  pbr.inputs[2].default_value = 0.0
  tr2 = m.node_tree.nodes.new("ShaderNodeBsdfTransparent")
  s2r = m.node_tree.nodes.new("ShaderNodeShaderToRGB")
  d3 = m.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
  d3.inputs[0].default_value = (0, 0, 0, 1)
  d3.inputs[1].default_value = 0
  m.node_tree.links.new(pbr.outputs[0], s2r.inputs[0])
  m.node_tree.links.new(s2r.outputs[0], mx3.inputs[0])
  m.node_tree.links.new(d3.outputs[0], mx3.inputs[1])
  m.node_tree.links.new(tr2.outputs[0], mx3.inputs[2])
  m.node_tree.links.new(mx3.outputs[0], out_e.inputs[0])
  return m



def create_planes(context):
  ambient = _ambient_mat()
  blue = _blue_mat()
  grey = _grey_mat()
  holdout = _holdout_mat()
  shadow = _shadow_mat()

  vll = context.view_layer.layer_collection
  context.view_layer.active_layer_collection = vll.children[COLLECTION_NAME]

  _make_plane(f"{PREFIX}Plane.ambient", location=(0, 0, -20), hide_render=True, hide_viewport=True, material=ambient)
  _make_plane(f"{PREFIX}Plane.blue", hide_render=True, hide_viewport=True, material=blue)
  _make_plane(f"{PREFIX}Plane.grey", hide_render=True, hide_viewport=True, material=grey)
  _make_plane(f"{PREFIX}Plane.holdout2", hide_render=True, hide_viewport=True, material=holdout)
  obj = _make_plane(f"{PREFIX}Plane.shadow2", hide_render=True, hide_viewport=True, shadow_catcher=True, material=shadow)
  obj.active_material.surface_render_method = "BLENDED"

  shadow_coll = vll.children[COLLECTION_NAME].children[f"{COLLECTION_NAME} Shadow"]
  context.view_layer.active_layer_collection = shadow_coll
  obj = _make_plane(f"{PREFIX}Plane.shadow", hide_render=True, hide_viewport=True, shadow_catcher=True, material=shadow)
  obj.active_material.surface_render_method = "BLENDED"

  holdout_coll = vll.children[COLLECTION_NAME].children[f"{COLLECTION_NAME} Holdout"]
  context.view_layer.active_layer_collection = holdout_coll
  _make_plane(f"{PREFIX}Plane.holdout", location=(0, 0, -0.015), hide_render=True, hide_viewport=True, material=holdout)
  holdout_coll.exclude = True


# ──────────────────────────────────────────────
# Compositor
# ──────────────────────────────────────────────
def create_compositor(context, props):
  scene = context.scene
  prefix = ALPHA_CONVERT_NAME
  alpha_group = bpy.data.node_groups.new(type="CompositorNodeTree", name=prefix)
  alpha_group.interface.new_socket(name="Image", in_out="INPUT", socket_type="NodeSocketColor")
  alpha_group.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
  alpha_group.interface.new_socket(name="Alpha", in_out="OUTPUT", socket_type="NodeSocketFloat")
  gi = alpha_group.nodes.new("NodeGroupInput")
  gi.location = (-400, 0)
  go = alpha_group.nodes.new("NodeGroupOutput")
  go.location = (400, 0)
  s_hsva = alpha_group.nodes.new("CompositorNodeSeparateColor")
  s_hsva.mode = "HSV"
  s_hsva.location = (-200, 200)
  c_hsva = alpha_group.nodes.new("CompositorNodeCombineColor")
  c_hsva.mode = "HSV"
  c_hsva.location = (200, 200)
  math_op = alpha_group.nodes.new("ShaderNodeMath")
  math_op.location = (0, 0)
  math_op.operation = "GREATER_THAN"
  math_op.inputs[1].default_value = 0.325
  alpha_group.links.new(gi.outputs[0], s_hsva.inputs[0])
  alpha_group.links.new(s_hsva.outputs[0], c_hsva.inputs[0])
  alpha_group.links.new(s_hsva.outputs[1], c_hsva.inputs[1])
  alpha_group.links.new(s_hsva.outputs[2], c_hsva.inputs[2])
  alpha_group.links.new(s_hsva.outputs[3], math_op.inputs[0])
  alpha_group.links.new(math_op.outputs[0], c_hsva.inputs[3])
  alpha_group.links.new(math_op.outputs[0], go.inputs[1])
  alpha_group.links.new(c_hsva.outputs[0], go.inputs[0])

  config = get_config(props.game, props.variant)

  node_tree = bpy.data.node_groups.new(name=COMP_TREE_NAME, type="CompositorNodeTree")
  nodes = node_tree.nodes
  links = node_tree.links

  rl = nodes.new("CompositorNodeRLayers")
  rl.location = (0, 0)
  go = nodes.new("NodeGroupOutput")
  go.location = (800, 0)
  node_tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")

  render_type = props.render_type

  if render_type == "DEFAULT":
    scene.render.film_transparent = False
    hue_mix = _create_remap_hue(context, nodes, links, rl, go, props) if props.remap_materials else None
    if hue_mix:
      links.new(rl.outputs[0], hue_mix.inputs['A'])
      links.new(hue_mix.outputs['Result'], go.inputs[0])
    else:
      links.new(rl.outputs[0], go.inputs[0])
    scene.render.image_settings.color_mode = "RGB"

  elif render_type == "PREVIEW":
    _wire_preview(context, node_tree, rl, go, links, nodes, props, config)

  elif render_type == "OBJECT":
    _wire_object_or_buildup(context, node_tree, rl, go, links, nodes, props)

  elif render_type == "BUILDUP":
    _wire_object_or_buildup(context, node_tree, rl, go, links, nodes, props)

  elif render_type == "SHADOW":
    _wire_shadow(node_tree, rl, go, links, nodes, props, config)

  scene.compositing_node_group = node_tree


def _create_remap_hue(context, nodes, links, rl_node, go, props):
  mat_names = [item.material.name for item in props.remap_materials if item.material]
  if not mat_names:
    return None

  crypto = nodes.new("CompositorNodeCryptomatteV2")
  layer_items = crypto.bl_rna.properties['layer_name'].enum_items
  material_layer = next((item.identifier for item in layer_items if 'Material' in item.identifier), None)
  if material_layer:
    if '.' not in material_layer:
      material_layer = context.view_layer.name + '.' + material_layer
    crypto.layer_name = material_layer
  crypto.matte_id = ",".join(mat_names)
  crypto.location = (go.location.x - 300, go.location.y - 100)

  if rl_node:
    links.new(rl_node.outputs[0], crypto.inputs[0])
    crypto_outputs = [o for o in rl_node.outputs if 'Crypto' in o.name]
    max_crypto = min(len(crypto_outputs), len(crypto.inputs) - 1)
    for i in range(max_crypto):
      links.new(crypto_outputs[i], crypto.inputs[i + 1])

  threshold = nodes.new("ShaderNodeMath")
  threshold.operation = "GREATER_THAN"
  threshold.inputs[1].default_value = 0.01
  threshold.location = (go.location.x - 200, go.location.y - 100)

  hue_mix = nodes.new("ShaderNodeMix")
  hue_mix.data_type = "RGBA"
  hue_mix.blend_type = "COLOR"
  hue_mix.location = (go.location.x - 100, go.location.y - 100)

  links.new(crypto.outputs[1], threshold.inputs[0])
  links.new(threshold.outputs[0], hue_mix.inputs[0])
  hue_mix.inputs['B'].default_value = props.remap_color

  return hue_mix


def _alpha_convert_node():
  return bpy.data.node_groups.get(ALPHA_CONVERT_NAME)


def _wire_object_or_buildup(context, tree, rl, go, links, nodes, props):
  bg_rgb = nodes.new("CompositorNodeRGB")
  bg_rgb.name = f"{PREFIX}BackgroundRGB"
  bg_rgb.outputs[0].default_value = props.background_color
  bg_rgb.location = (0, 200)

  if props.transparent_bg:
    if props.aa_against_bg:
      hue_mix = _create_remap_hue(context, nodes, links, rl, go, props) if props.remap_materials else None
      if hue_mix:
        links.new(rl.outputs[0], hue_mix.inputs['A'])
        links.new(hue_mix.outputs['Result'], go.inputs[0])
      else:
        links.new(rl.outputs[0], go.inputs[0])
      scene = bpy.context.scene
      scene.render.film_transparent = True
      scene.render.image_settings.color_mode = "RGBA"
      scene.render.image_settings.file_format = "PNG"
    else:
      ac = _alpha_convert_node()
      ac_node = nodes.new("CompositorNodeGroup")
      ac_node.node_tree = ac
      ac_node.location = (200, 0)
      ao = nodes.new("CompositorNodeAlphaOver")
      ao.location = (400, 0)
      ao.inputs[4].default_value = True
      links.new(rl.outputs[0], ac_node.inputs[0])
      hue_mix = _create_remap_hue(context, nodes, links, rl, go, props) if props.remap_materials else None
      if hue_mix:
        links.new(ac_node.outputs[0], hue_mix.inputs['A'])
        links.new(hue_mix.outputs['Result'], ao.inputs[1])
      else:
        links.new(ac_node.outputs[0], ao.inputs[1])
      links.new(bg_rgb.outputs[0], ao.inputs[0])
      links.new(ao.outputs[0], go.inputs[0])
      scene = bpy.context.scene
      scene.render.film_transparent = True
      scene.render.image_settings.color_mode = "RGBA"
      scene.render.image_settings.file_format = "PNG"
  else:
    ac = _alpha_convert_node()
    ac_node = nodes.new("CompositorNodeGroup")
    ac_node.node_tree = ac
    ac_node.location = (200, 0)
    ao = nodes.new("CompositorNodeAlphaOver")
    ao.location = (400, 0)
    ao.inputs[4].default_value = True
    links.new(rl.outputs[0], ac_node.inputs[0])
    hue_mix = _create_remap_hue(context, nodes, links, rl, go, props) if props.remap_materials else None
    if hue_mix:
      links.new(ac_node.outputs[0], hue_mix.inputs['A'])
      links.new(hue_mix.outputs['Result'], ao.inputs[1])
    else:
      links.new(ac_node.outputs[0], ao.inputs[1])
    links.new(bg_rgb.outputs[0], ao.inputs[0])
    links.new(ao.outputs[0], go.inputs[0])
    scene = bpy.context.scene
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = "RGB"


def _wire_preview(context, tree, rl, go, links, nodes, props, config):
  bg_rgb = nodes.new("CompositorNodeRGB")
  bg_rgb.name = f"{PREFIX}BackgroundRGB"
  if props.transparent_bg:
    bg_rgb.outputs[0].default_value = (0, 0, 0, 0)
  else:
    bg_rgb.outputs[0].default_value = props.background_color
  bg_rgb.location = (0, 200)

  shadow_rgb = nodes.new("CompositorNodeRGB")
  shadow_rgb.name = f"{PREFIX}ShadowRGB"
  shadow_rgb.outputs[0].default_value = props.shadow_color
  shadow_rgb.location = (0, -200)

  ac = _alpha_convert_node()
  ac_node = nodes.new("CompositorNodeGroup")
  ac_node.node_tree = ac
  ac_node.location = (200, 0)

  crypto = nodes.new("CompositorNodeCryptomatteV2")
  crypto.matte_id = f"{PREFIX}Plane.shadow"
  crypto.location = (200, -300)

  threshold = nodes.new("ShaderNodeMath")
  threshold.operation = "GREATER_THAN"
  threshold.inputs[1].default_value = 0.72
  threshold.location = (300, -300)

  mask = nodes.new("ShaderNodeMath")
  mask.operation = "MULTIPLY"
  mask.location = (400, -300)

  opacity = nodes.new("ShaderNodeMath")
  opacity.operation = "MULTIPLY"
  opacity.inputs[1].default_value = props.shadow_opacity
  opacity.location = (500, -300)

  ao_shadow = nodes.new("CompositorNodeAlphaOver")
  ao_shadow.location = (600, -200)
  ao_shadow.inputs[4].default_value = True

  ao_tint = nodes.new("CompositorNodeAlphaOver")
  ao_tint.location = (700, 0)
  ao_tint.inputs[4].default_value = True

  ao = nodes.new("CompositorNodeAlphaOver")
  ao.location = (800, 0)
  ao.inputs[4].default_value = True

  bg_input = bg_rgb.outputs[0]
  if props.use_bg_image and props.bg_image_path:
    abs_path = bpy.path.abspath(props.bg_image_path)
    if os.path.isfile(abs_path):
      img = bpy.data.images.load(abs_path, check_existing=True)
      img_node = nodes.new("CompositorNodeImage")
      img_node.image = img
      img_node.location = (0, 400)
      bg_input = img_node.outputs[0]

  links.new(rl.outputs[0], ac_node.inputs[0])
  links.new(rl.outputs[0], crypto.inputs[0])

  links.new(crypto.outputs[1], threshold.inputs[0])
  links.new(threshold.outputs[0], mask.inputs[0])
  links.new(ac_node.outputs[1], mask.inputs[1])
  links.new(mask.outputs[0], opacity.inputs[0])

  links.new(bg_input, ao_shadow.inputs[0])
  links.new(shadow_rgb.outputs[0], ao_shadow.inputs[1])
  links.new(opacity.outputs[0], ao_shadow.inputs[2])

  hue_mix = _create_remap_hue(context, nodes, links, rl, go, props) if props.remap_materials else None
  if hue_mix:
    links.new(ac_node.outputs[0], hue_mix.inputs['A'])
    links.new(hue_mix.outputs['Result'], ao_tint.inputs[0])
  else:
    links.new(ac_node.outputs[0], ao_tint.inputs[0])
  links.new(ao_shadow.outputs[0], ao_tint.inputs[1])
  links.new(mask.outputs[0], ao_tint.inputs[2])

  links.new(ao_tint.outputs[0], ao.inputs[1])
  links.new(bg_input, ao.inputs[0])
  links.new(ao.outputs[0], go.inputs[0])

  scene = bpy.context.scene
  scene.render.film_transparent = True
  if props.transparent_bg:
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.file_format = "PNG"
  else:
    scene.render.image_settings.color_mode = "RGB"


def _wire_shadow(tree, rl, go, links, nodes, props, config):
  bg_rgb = nodes.new("CompositorNodeRGB")
  bg_rgb.name = f"{PREFIX}BackgroundRGB"
  if props.transparent_bg:
    bg_rgb.outputs[0].default_value = (0, 0, 0, 0)
  else:
    bg_rgb.outputs[0].default_value = props.background_color
  bg_rgb.location = (0, 200)

  crypto = nodes.new("CompositorNodeCryptomatteV2")
  matte_target = f"{PREFIX}Plane.shadow" if props.engine == "CYCLES" else f"{PREFIX}Plane.holdout"
  crypto.matte_id = matte_target
  crypto.location = (200, 0)

  sep = nodes.new("CompositorNodeSeparateColor")
  sep.mode = "HSV"
  sep.location = (400, 0)

  invert = nodes.new("CompositorNodeInvert")
  invert.location = (600, 0)

  screen = nodes.new("ShaderNodeMix")
  screen.data_type = "RGBA"
  screen.blend_type = "SCREEN"
  screen.inputs[0].default_value = 1
  screen.location = (800, 0)

  multiply = nodes.new("ShaderNodeMix")
  multiply.data_type = "RGBA"
  multiply.blend_type = "MULTIPLY"
  multiply.inputs[0].default_value = 1
  multiply.location = (1000, 0)

  cr = nodes.new("ShaderNodeValToRGB")
  cr.location = (1200, 0)
  cr.color_ramp.elements[0].position = config.colorramp_position01
  cr.color_ramp.elements[0].color = (props.shadow_color[0], props.shadow_color[1], props.shadow_color[2], 0)
  cr.color_ramp.elements[1].position = config.colorramp_position02
  cr.color_ramp.elements[1].color = (props.shadow_color[0], props.shadow_color[1], props.shadow_color[2], 1)

  ao = nodes.new("CompositorNodeAlphaOver")
  ao.location = (1400, 0)
  ao.inputs[4].default_value = True

  ac = _alpha_convert_node()
  ac_node = nodes.new("CompositorNodeGroup")
  ac_node.node_tree = ac
  ac_node.location = (200, 300)

  links.new(rl.outputs[2], crypto.inputs[0])
  links.new(crypto.outputs[2], sep.inputs[0])
  links.new(sep.outputs[1], invert.inputs[0])
  links.new(crypto.outputs[1], screen.inputs[6])
  links.new(invert.outputs[0], screen.inputs[7])
  links.new(screen.outputs[2], multiply.inputs[7])
  links.new(rl.outputs[0], ac_node.inputs[0])
  links.new(ac_node.outputs[1], multiply.inputs[6])
  links.new(multiply.outputs[2], cr.inputs[0])
  links.new(bg_rgb.outputs[0], ao.inputs[0])
  links.new(cr.outputs[0], ao.inputs[1])
  links.new(ao.outputs[0], go.inputs[0])

  scene = bpy.context.scene
  scene.render.film_transparent = True
  scene.render.image_settings.color_mode = "RGBA"


# ──────────────────────────────────────────────
# Render settings
# ──────────────────────────────────────────────
def apply_initial_settings(context, props):
  config = get_config(props.game, props.variant)
  scene = context.scene
  scene.frame_start = 0
  scene.frame_end = 11
  scene.render.fps = 10
  scene.render.dither_intensity = 0
  scene.render.image_settings.compression = 90
  scene.render.image_settings.file_format = "PNG"
  scene.unit_settings.system = "NONE"
  scene.view_settings.view_transform = "Standard"
  scene.view_settings.look = "None"
  scene.view_settings.exposure = 0
  props.is_shadow_filter_saved = False

  if props.engine == "CYCLES":
    scene.render.filter_size = 0.0
    scene.cycles.device = "GPU"
    scene.cycles.filter_width = config.cycles_filter_width
    scene.cycles.max_bounces = config.cycles_max_bounces
    scene.cycles.pixel_filter_type = "BLACKMAN_HARRIS"
    scene.cycles.preview_samples = config.cycles_preview_samples
    scene.cycles.samples = config.cycles_samples
    scene.cycles.adaptive_min_samples = config.cycles_adaptive_min_samples
    scene.cycles.sample_clamp_indirect = 0.05
    scene.cycles.transmission_bounces = 8
    scene.cycles.volume_bounces = 1
    scene.cycles.use_denoising = True
    scene.cycles.denoising_use_gpu = True
  else:
    scene.render.filter_size = 0.7
    scene.eevee.use_shadows = True

  vl = context.view_layer
  vl.cycles.denoising_store_passes = True
  vl.use_pass_cryptomatte_asset = True
  vl.pass_cryptomatte_depth = 2

  for workspace in bpy.data.workspaces:
    for screen in workspace.screens:
      for area in screen.areas:
        if area.type == "VIEW_3D":
          for space in area.spaces:
            if space.type == "VIEW_3D":
              space.shading.use_scene_lights = True
              space.shading.use_scene_world = True


def apply_render_settings(context, props):
  config = get_config(props.game, props.variant)
  scene = context.scene
  scene.render.resolution_x = config.resolution[0]
  scene.render.resolution_y = config.resolution[1]
  scene.render.use_single_layer = True

  if props.render_type == "SHADOW":
    if not props.is_shadow_filter_saved:
      props.saved_filter_size = scene.render.filter_size
      props.saved_filter_width = scene.cycles.filter_width if props.engine == "CYCLES" else 0.0
      props.is_shadow_filter_saved = True
    scene.render.use_single_layer = False
    scene.render.filter_size = 0.01
    if props.engine == "CYCLES":
      scene.cycles.filter_width = 0.01
  else:
    if props.is_shadow_filter_saved:
      scene.render.filter_size = props.saved_filter_size
      if props.engine == "CYCLES":
        scene.cycles.filter_width = props.saved_filter_width
      props.is_shadow_filter_saved = False


# ──────────────────────────────────────────────
# Apply render type visibility
# ──────────────────────────────────────────────
# Visibility dicts: 1 = hide_render=True (hidden), 0 = hide_render=False (visible)
# Order: holdout, holdout2, shadow, shadow2, blue, grey, ambient
RENDER_TYPE_VIS = {
  "DEFAULT":   {"holdout": 1, "holdout2": 1, "shadow": 1, "shadow2": 1, "blue": 1, "grey": 0, "ambient": 1},
  "PREVIEW": {"holdout": 0, "holdout2": 1, "shadow": 0, "shadow2": 1, "blue": 1, "grey": 1, "ambient": 1},
  "OBJECT":  {"holdout": 1, "holdout2": 1, "shadow": 1, "shadow2": 1, "blue": 1, "grey": 1, "ambient": 0},
  "BUILDUP": {"holdout": 1, "holdout2": 0, "shadow": 1, "shadow2": 1, "blue": 1, "grey": 1, "ambient": 1},
  "SHADOW":  {"holdout": 0, "holdout2": 1, "shadow": 0, "shadow2": 1, "blue": 1, "grey": 1, "ambient": 1},
}


def apply_render_type_visibility(context):
  props = context.scene.cc_toolkit
  vis = RENDER_TYPE_VIS.get(props.render_type, RENDER_TYPE_VIS["OBJECT"])
  for plane_id in ("holdout", "holdout2", "shadow", "shadow2", "blue", "grey", "ambient"):
    hide_val = bool(vis.get(plane_id, 1))
    obj = bpy.data.objects.get(f"{PREFIX}Plane.{plane_id}")
    if obj:
      obj.hide_render = hide_val

  vll = context.view_layer.layer_collection
  for child in vll.children[f"{COLLECTION_NAME}"].children:
    if child.name == f"{COLLECTION_NAME} Holdout":
      child.exclude = bool(vis.get("holdout", 1))
      break

  sun = bpy.data.objects.get(f"{PREFIX}Sun")
  if sun:
    sun.hide_render = True if props.engine == "CYCLES" else False
