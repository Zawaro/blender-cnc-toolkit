import bpy
from . import VERSION_STRING
from .operators import CNC_OT_render_shadow


class VIEW3D_PT_cc_toolkit(bpy.types.Panel):
  bl_idname = "VIEW3D_PT_cc_toolkit"
  bl_label = "C&C Toolkit"
  bl_category = "C&C Toolkit"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"

  def draw(self, context):
    layout = self.layout
    props = context.scene.cc_toolkit

    row = layout.row()
    row.enabled = False
    row.label(text=VERSION_STRING)
    layout.separator()

    if not props.template_generated:
      self._draw_initial(layout, props)
    else:
      self._draw_active(layout, props, context)

  def _draw_initial(self, layout, props):
    layout.prop(props, "game")
    layout.prop(props, "variant")
    layout.prop(props, "engine")
    if props.game in {"RA1", "RM", "D2K"}:
      layout.prop(props, "camera_mode")
    layout.separator()
    layout.operator("ccnc.generate_template")

  def _draw_active(self, layout, props, context):
    layout.prop(props, "game")
    layout.prop(props, "variant")
    layout.prop(props, "engine")
    if props.game in {"RA1", "RM", "D2K"}:
      layout.prop(props, "camera_mode")
    layout.separator()
    layout.operator("ccnc.purge_template")
    layout.separator()

    layout.label(text="Render Type")
    layout.prop(props, "render_type", text="")
    layout.prop(props, "aa_against_bg")
    layout.prop(props, "transparent_bg")
    layout.separator()

    layout.prop(props, "background_color")
    layout.prop(props, "shadow_color")
    if props.render_type == "PREVIEW":
      layout.prop(props, "shadow_opacity")
    layout.separator()

    layout.label(text="Remap Materials")
    row = layout.row()
    row.prop(props, "remap_material_picker", text="")
    row.operator("ccnc.add_remap_material", text="Add", icon="ADD")

    for i, item in enumerate(props.remap_materials):
      row = layout.row()
      row.prop(item, "material", text="")
      op = row.operator("ccnc.remove_remap_material", text="", icon="X")
      op.index = i

    if props.remap_materials:
      layout.operator("ccnc.clear_remap_materials", text="Clear All", icon="X")
      layout.prop(props, "remap_color")

    layout.separator()

    if props.render_type == "PREVIEW":
      box = layout.box()
      box.prop(props, "use_bg_image")
      if props.use_bg_image:
        box.prop(props, "bg_image_path")
      layout.separator()

    layout.prop(props, "frame_offset")
    layout.prop(props, "output_path")
    layout.separator()

    is_rendering = bool(CNC_OT_render_shadow._queue) or bpy.app.is_job_running("RENDER")

    if is_rendering:
      row = layout.row()
      row.operator("ccnc.cancel_render", text="Stop Render", icon="CANCEL")
    else:
      row = layout.row()
      if props.render_type in {"OBJECT", "BUILDUP"}:
        layout.prop(props, "render_shadow_with_animation")
      row.operator("ccnc.render", text="Render Current", icon="RENDER_STILL")
      row.operator("ccnc.render_shadow", text="Render Animation", icon="SEQUENCE")


class VIEW3D_PT_cc_toolkit_crop_canvas(bpy.types.Panel):
  bl_label = "Crop Canvas"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"
  bl_category = "C&C Toolkit"

  def draw_header(self, context):
    layout = self.layout
    crop = context.scene.cc_crop_canvas
    layout.prop(crop, "use_crop_canvas", text="")

  def draw(self, context):
    layout = self.layout
    crop = context.scene.cc_crop_canvas
    row = layout.row()
    row.enabled = crop.use_crop_canvas
    row.prop(crop, "x_int")
    row.prop(crop, "y_int")
