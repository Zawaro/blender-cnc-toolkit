import bpy

GAME_ITEMS = [
  ("RA2", "Red Alert 2", ""),
  ("TS", "Tiberian Sun", ""),
  ("RW", "ReWire", ""),
  ("RA1", "Red Alert / Tiberian Dawn", ""),
  ("RM", "C&C Remastered", ""),
  ("D2K", "Dune 2000", ""),
]

VARIANT_ITEMS = [
  ("BASE", "Base", ""),
  ("INF", "Infantry", ""),
  ("FX", "Effects", ""),
]

ENGINE_ITEMS = [
  ("CYCLES", "Cycles", ""),
  ("EEVEE", "Eevee", ""),
]

CAMERA_MODE_ITEMS = [
  ("PERSP", "Perspective", "Original 3D perspective camera view"),
  ("ORTHO", "Isometric", "Standard C&C isometric camera view"),
]

RENDER_TYPE_ITEMS = [
  ("DEFAULT", "Default", ""),
  ("PREVIEW", "Preview", ""),
  ("OBJECT", "Object", ""),
  ("BUILDUP", "Buildup", ""),
  ("SHADOW", "Shadow", ""),
]


def _rebuild(instance, context):
  from . import scene_builder
  scene_builder.rebuild_all(context)


def _rebuild_if_generated(instance, context):
  if not context.scene.cc_toolkit.template_generated:
    return
  from . import scene_builder
  scene_builder.rebuild_all(context)


class CncToolkitProperties(bpy.types.PropertyGroup):
  game: bpy.props.EnumProperty(
    name="Game",
    description="C&C game target",
    items=GAME_ITEMS,
    default="RA2",
    update=_rebuild_if_generated,
  )

  variant: bpy.props.EnumProperty(
    name="Variant",
    description="Scene variant type",
    items=VARIANT_ITEMS,
    default="BASE",
    update=_rebuild_if_generated,
  )

  engine: bpy.props.EnumProperty(
    name="Engine",
    description="Render engine",
    items=ENGINE_ITEMS,
    default="CYCLES",
    update=_rebuild_if_generated,
  )

  camera_mode: bpy.props.EnumProperty(
    name="Camera Mode",
    description="Perspective (original 3D) or Isometric (standard C&C)",
    items=CAMERA_MODE_ITEMS,
    default="ORTHO",
    update=_rebuild_if_generated,
  )

  render_type: bpy.props.EnumProperty(
    name="Render Type",
    description="Frame render type",
    items=RENDER_TYPE_ITEMS,
    default="DEFAULT",
    update=_rebuild_if_generated,
  )

  frame_offset: bpy.props.IntProperty(
    name="Frame Offset",
    description="Number added to output frame filenames for single-pass Render. Auto-calculated for Render + Shadow.",
    default=0,
    min=0,
    max=9999,
  )

  render_shadow_with_animation: bpy.props.BoolProperty(
    name="Render shadow with animation",
    description="When enabled, Render Animation also renders the Shadow pass after the primary pass",
    default=False,
  )

  aa_against_bg: bpy.props.BoolProperty(
    name="Anti-aliasing against background",
    description="Bypass Alpha Convert node group for smooth anti-aliased edges via film_transparent",
    default=False,
    update=_rebuild_if_generated,
  )

  transparent_bg: bpy.props.BoolProperty(
    name="Transparent background",
    description="Output RGBA (alpha channel present) or RGB (solid background)",
    default=False,
    update=_rebuild_if_generated,
  )

  background_color: bpy.props.FloatVectorProperty(
    name="Background Color",
    description="Solid background color for non-transparent renders",
    subtype="COLOR",
    size=4,
    default=(0, 0, 1, 1),
    min=0.0,
    max=1.0,
    update=_rebuild_if_generated,
  )

  shadow_color: bpy.props.FloatVectorProperty(
    name="Shadow Color",
    description="Color tint applied to shadow-only renders",
    subtype="COLOR",
    size=4,
    default=(0, 0, 0, 1),
    min=0.0,
    max=1.0,
    update=_rebuild_if_generated,
  )

  use_bg_image: bpy.props.BoolProperty(
    name="Background Image",
    description="Use an image as the background instead of the solid color",
    default=False,
    update=_rebuild_if_generated,
  )

  bg_image_path: bpy.props.StringProperty(
    name="Background Image",
    default="",
    subtype="FILE_PATH",
    update=_rebuild_if_generated,
  )

  shadow_opacity: bpy.props.FloatProperty(
    name="Shadow Opacity",
    description="Opacity of the shadow tint in Preview mode",
    default=1.0,
    min=0.0,
    max=1.0,
    update=_rebuild_if_generated,
  )

  output_path: bpy.props.StringProperty(
    name="Output",
    default="/tmp/",
    subtype="DIR_PATH",
  )

  template_generated: bpy.props.BoolProperty(
    name="Template Generated",
    default=False,
  )

  saved_state: bpy.props.StringProperty(
    name="Saved State",
    description="JSON snapshot of pre-template scene state for purge restoration",
    default="",
  )

  saved_filter_size: bpy.props.FloatProperty(
    name="Saved Filter Size",
    description="Stored filter size before SHADOW override",
    default=0.0,
  )

  saved_filter_width: bpy.props.FloatProperty(
    name="Saved Filter Width",
    description="Stored Cycles filter width before SHADOW override",
    default=0.9,
  )

  is_shadow_filter_saved: bpy.props.BoolProperty(
    name="Shadow Filter Saved",
    description="Whether filter values have been saved before SHADOW override",
    default=False,
  )
