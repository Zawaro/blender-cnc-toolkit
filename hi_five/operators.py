from __future__ import annotations

import os
import bpy

from . import scene_builder


class CNC_OT_generate_template(bpy.types.Operator):
  bl_idname = "ccnc.generate_template"
  bl_label = "Generate Template"
  bl_description = "Build the C&C template scene with current settings"

  def execute(self, context):
    props = context.scene.cc_toolkit
    if not props.template_generated:
      scene_builder.save_scene_state(context)
      scene_builder.apply_initial_settings(context, props)
    scene_builder.rebuild_all(context)
    props.template_generated = True
    return {"FINISHED"}


class CNC_OT_purge_template(bpy.types.Operator):
  bl_idname = "ccnc.purge_template"
  bl_label = "Purge Template"
  bl_description = "Remove all template data and restore pre-template state"

  def execute(self, context):
    props = context.scene.cc_toolkit
    scene_builder.clear_template(context)
    scene_builder.restore_scene_state(context)
    props.template_generated = False
    props.saved_state = ""
    return {"FINISHED"}


class CNC_OT_render(bpy.types.Operator):
  bl_idname = "ccnc.render"
  bl_label = "Render Current"
  bl_description = "Render the current frame with optional frame offset"

  def execute(self, context):
    props = context.scene.cc_toolkit
    scene = context.scene
    out_dir = bpy.path.abspath(props.output_path)
    offset = props.frame_offset
    filepath = os.path.join(out_dir, f"render_{offset + scene.frame_current:04d}.png")

    scene.render.filepath = filepath
    scene_builder.apply_render_type_visibility(context)
    bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)
    return {"FINISHED"}


class CNC_OT_render_shadow(bpy.types.Operator):
  bl_idname = "ccnc.render_shadow"
  bl_label = "Render Animation"
  bl_description = (
    "Render all frames. If shadow option is on, renders primary pass then shadow pass."
  )

  _queue: list[tuple[str, int, str]] = []
  _original_rt: str = ""
  _frame_count: int = 0

  def execute(self, context):
    props = context.scene.cc_toolkit
    scene = context.scene
    out_dir = bpy.path.abspath(props.output_path)

    CNC_OT_render_shadow._original_rt = props.render_type
    CNC_OT_render_shadow._frame_count = scene.frame_end - scene.frame_start + 1

    if props.render_shadow_with_animation and props.render_type in {
      "OBJECT",
      "BUILDUP",
    }:
      passes = [props.render_type, "SHADOW"]
    else:
      passes = [props.render_type]

    CNC_OT_render_shadow._queue = []
    frame_offset = 0
    for rt in passes:
      for f in range(scene.frame_start, scene.frame_end + 1):
        filepath = os.path.join(out_dir, f"render_{frame_offset + f:04d}.png")
        CNC_OT_render_shadow._queue.append((rt, f, filepath))
      frame_offset += CNC_OT_render_shadow._frame_count

    CNC_OT_render_shadow._render_next(context)
    return {"FINISHED"}

  @classmethod
  def _render_next(cls, context):
    if not cls._queue:
      cls._cleanup(context)
      return

    rt, f, filepath = cls._queue.pop(0)
    props = context.scene.cc_toolkit
    scene = context.scene

    props.render_type = rt
    scene_builder.apply_render_type_visibility(context)
    scene.frame_current = f
    scene.render.filepath = filepath

    bpy.app.handlers.render_complete.append(cls._on_frame_done)
    bpy.app.handlers.render_cancel.append(cls._on_cancelled)
    bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)

  @classmethod
  def _cleanup(cls, context):
    props = context.scene.cc_toolkit
    props.render_type = cls._original_rt
    if cls._on_frame_done in bpy.app.handlers.render_complete:
      bpy.app.handlers.render_complete.remove(cls._on_frame_done)
    if cls._on_cancelled in bpy.app.handlers.render_cancel:
      bpy.app.handlers.render_cancel.remove(cls._on_cancelled)
    if bpy.app.timers.is_registered(cls._defer_render):
      bpy.app.timers.unregister(cls._defer_render)
    cls._queue.clear()

  @classmethod
  def _on_frame_done(cls, *args):
    if cls._on_cancelled in bpy.app.handlers.render_cancel:
      bpy.app.handlers.render_cancel.remove(cls._on_cancelled)
    bpy.app.handlers.render_complete.remove(cls._on_frame_done)

    if cls._queue:
      bpy.app.timers.register(cls._defer_render, first_interval=0.1)

  @classmethod
  def _on_cancelled(cls, *args):
    scene = args[0] if args else bpy.context.scene
    cls._cleanup(scene)
    print("Render cancelled by user.")

  @classmethod
  def _defer_render(cls):
    if bpy.app.is_job_running("RENDER"):
      return 0.1
    if cls._queue:
      cls._render_next(bpy.context)
    return None


class CNC_OT_cancel_render(bpy.types.Operator):
  bl_idname = "ccnc.cancel_render"
  bl_label = "Stop Render"
  bl_description = "Stop the ongoing render animation"

  def execute(self, context):
    CNC_OT_render_shadow._cleanup(context)
    for area in context.screen.areas:
      if area.type == "VIEW_3D":
        area.tag_redraw()
    return {"FINISHED"}


class CNC_OT_add_remap_material(bpy.types.Operator):
  bl_idname = "ccnc.add_remap_material"
  bl_label = "Add Remap Material"
  bl_description = (
    "Add the selected material to the remap list (toolkit materials excluded)"
  )

  def execute(self, context):
    props = context.scene.cc_toolkit
    for i in range(len(props.remap_materials) - 1, -1, -1):
      if not props.remap_materials[i].material:
        props.remap_materials.remove(i)
    if props.remap_material_picker:
      if props.remap_material_picker.name.startswith("_CNC_"):
        self.report({"WARNING"}, "Cannot add toolkit materials")
        return {"CANCELLED"}
      if any(
        item.material == props.remap_material_picker for item in props.remap_materials
      ):
        self.report({"WARNING"}, "Material already in list")
        return {"CANCELLED"}
      item = props.remap_materials.add()
      item.material = props.remap_material_picker
      props.remap_material_picker = None
      if props.template_generated:
        scene_builder.rebuild_compositor(context)
    return {"FINISHED"}


class CNC_OT_remove_remap_material(bpy.types.Operator):
  bl_idname = "ccnc.remove_remap_material"
  bl_label = "Remove Remap Material"
  bl_description = "Remove a material from the remap list"

  index: bpy.props.IntProperty()

  def execute(self, context):
    props = context.scene.cc_toolkit
    if 0 <= self.index < len(props.remap_materials):
      props.remap_materials.remove(self.index)
      if props.template_generated:
        scene_builder.rebuild_compositor(context)
    return {"FINISHED"}


class CNC_OT_clear_remap_materials(bpy.types.Operator):
  bl_idname = "ccnc.clear_remap_materials"
  bl_label = "Clear Remap Materials"
  bl_description = "Remove all materials from the remap list"

  def execute(self, context):
    props = context.scene.cc_toolkit
    if props.remap_materials:
      props.remap_materials.clear()
      if props.template_generated:
        scene_builder.rebuild_compositor(context)
    return {"FINISHED"}
