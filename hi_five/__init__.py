bl_info = {
  "name": "Blender C&C Toolkit (HiFive)",
  "author": "Zawaro",
  "version": (0, 2, 1),
  "blender": (5, 0, 0),
  "location": "View3D > Sidebar > C&C Toolkit",
  "description": "All-in-one toolkit to render C&C assets.",
  "category": "Generic",
}

import os

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
from .panel import VIEW3D_PT_cc_toolkit, VIEW3D_PT_cc_toolkit_crop_canvas
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
  VIEW3D_PT_cc_toolkit_crop_canvas,
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


def register():
  for cls in classes:
    register_class(cls)

  bpy.types.Scene.cc_crop_canvas = PointerProperty(type=CropCanvasProperties)
  bpy.types.Scene.cc_toolkit = PointerProperty(type=CncToolkitProperties)

  if crop_canvas_monitor_handler not in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.append(crop_canvas_monitor_handler)


def unregister():
  for cls in reversed(classes):
    unregister_class(cls)

  del bpy.types.Scene.cc_toolkit
  del bpy.types.Scene.cc_crop_canvas

  if crop_canvas_monitor_handler in bpy.app.handlers.depsgraph_update_post:
    bpy.app.handlers.depsgraph_update_post.remove(crop_canvas_monitor_handler)
