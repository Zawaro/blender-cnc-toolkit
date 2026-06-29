import os

bl_info = {
  "name": "Blender C&C Toolkit (CyclesX)",
  "author": "Zawaro",
  "version": (0, 3, 0),
  "blender": (3, 0, 0),
  "location": "View3D > Sidebar > C&C Toolkit",
  "description": "All-in-one toolkit to render C&C assets.",
  "category": "Generic",
}

BUILD_NUMBER = "0"
try:
  from ._build import BUILD_NUMBER as _BN
  BUILD_NUMBER = _BN
except ImportError:
  pass

VERSION_STRING = f"{'.'.join(str(v) for v in bl_info['version'])} (build {BUILD_NUMBER})"

import bpy
from bpy.utils import register_class
from bpy.props import PointerProperty
from bpy.utils import unregister_class

from .properties import CncToolkitProperties, RemapMaterialItem

# Render state tracking - defined BEFORE panel import to avoid circular import
_is_rendering = False


@bpy.app.handlers.persistent
def _on_render_init(scene):
  global _is_rendering
  _is_rendering = True


@bpy.app.handlers.persistent
def _on_render_end(scene):
  global _is_rendering
  _is_rendering = False


# Panel imports - AFTER _is_rendering is defined
from .panel import (
  VIEW3D_PT_cc_toolkit,
  VIEW3D_PT_cc_toolkit_render,
  VIEW3D_PT_cc_toolkit_bg_image,
  VIEW3D_PT_cc_toolkit_materials,
  VIEW3D_PT_cc_toolkit_boolean,
  VIEW3D_PT_cc_toolkit_output,
  VIEW3D_PT_cc_toolkit_crop_canvas,
  VIEW3D_PT_cc_toolkit_options,
  VIEW3D_PT_cc_toolkit_denoise,
)
from .operators import (
  CNC_OT_generate_template,
  CNC_OT_purge_template,
  CNC_OT_render,
  CNC_OT_render_shadow,
  CNC_OT_cancel_render,
  CNC_OT_add_remap_material,
  CNC_OT_remove_remap_material,
  CNC_OT_clear_remap_materials,
)
from .crop_canvas import (
  RENDER_PT_crop_canvas_format,
  CropCanvasProperties,
  crop_canvas_monitor,
)

classes = (
  CropCanvasProperties,
  RemapMaterialItem,
  CncToolkitProperties,
  RENDER_PT_crop_canvas_format,
  VIEW3D_PT_cc_toolkit,
  VIEW3D_PT_cc_toolkit_render,
  VIEW3D_PT_cc_toolkit_bg_image,
  VIEW3D_PT_cc_toolkit_materials,
  VIEW3D_PT_cc_toolkit_boolean,
  VIEW3D_PT_cc_toolkit_output,
  VIEW3D_PT_cc_toolkit_crop_canvas,
  VIEW3D_PT_cc_toolkit_options,
  VIEW3D_PT_cc_toolkit_denoise,
  CNC_OT_generate_template,
  CNC_OT_purge_template,
  CNC_OT_render,
  CNC_OT_render_shadow,
  CNC_OT_cancel_render,
  CNC_OT_add_remap_material,
  CNC_OT_remove_remap_material,
  CNC_OT_clear_remap_materials,
)


def crop_canvas_monitor_handler(scene, depsgraph=None):
  crop_canvas_monitor(scene)


def _write_guide():
  addon_dir = os.path.dirname(os.path.realpath(__file__))
  guide_path = os.path.join(addon_dir, "GUIDE.md")
  if os.path.isfile(guide_path):
    with open(guide_path, "r") as f:
      content = f.read()
    text = bpy.data.texts.get("C&C Toolkit Guide")
    if not text:
      text = bpy.data.texts.new("C&C Toolkit Guide")
    text.clear()
    text.write(content)
    text.filepath = ""


def register():
  for cls in classes:
    register_class(cls)

  bpy.types.Scene.cc_crop_canvas = PointerProperty(type=CropCanvasProperties)
  bpy.types.Scene.cc_toolkit = PointerProperty(type=CncToolkitProperties)

  if crop_canvas_monitor_handler not in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.append(crop_canvas_monitor_handler)

  bpy.app.timers.register(_write_guide, first_interval=0.1)

  if _on_render_init not in bpy.app.handlers.render_init:
    bpy.app.handlers.render_init.append(_on_render_init)
  if _on_render_end not in bpy.app.handlers.render_complete:
    bpy.app.handlers.render_complete.append(_on_render_end)
  if _on_render_end not in bpy.app.handlers.render_cancel:
    bpy.app.handlers.render_cancel.append(_on_render_end)


def unregister():
  for cls in reversed(classes):
    unregister_class(cls)

  del bpy.types.Scene.cc_toolkit
  del bpy.types.Scene.cc_crop_canvas

  if crop_canvas_monitor_handler in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.remove(crop_canvas_monitor_handler)

  if _on_render_init in bpy.app.handlers.render_init:
    bpy.app.handlers.render_init.remove(_on_render_init)
  if _on_render_end in bpy.app.handlers.render_complete:
    bpy.app.handlers.render_complete.remove(_on_render_end)
  if _on_render_end in bpy.app.handlers.render_cancel:
    bpy.app.handlers.render_cancel.remove(_on_render_end)


if __name__ == "__main__":
  register()
