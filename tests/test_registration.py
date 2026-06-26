import importlib

import bpy
import pytest


@pytest.fixture(scope="module")
def addon(addon_name):
  return importlib.import_module(addon_name)


class TestAddonInstalled:
  def test_scene_has_cc_toolkit(self):
    assert hasattr(bpy.types.Scene, "cc_toolkit")

  def test_scene_has_cc_crop_canvas(self):
    assert hasattr(bpy.types.Scene, "cc_crop_canvas")


class TestRegisterUnregister:
  def test_handler_not_duplicated(self, addon):
    handler = addon.crop_canvas_monitor_handler
    count = bpy.app.handlers.depsgraph_update_post.count(handler)
    assert count <= 1


class TestOperatorsRegistered:
  EXPECTED_OPERATORS = [
    "CNC_OT_generate_template",
    "CNC_OT_purge_template",
    "CNC_OT_render",
    "CNC_OT_render_shadow",
    "CNC_OT_cancel_render",
    "CNC_OT_add_remap_material",
    "CNC_OT_remove_remap_material",
    "CNC_OT_clear_remap_materials",
  ]

  @pytest.mark.parametrize("op_name", EXPECTED_OPERATORS)
  def test_operator_exists(self, addon, op_name):
    assert hasattr(addon, op_name)
    cls = getattr(addon, op_name)
    assert hasattr(cls, "bl_idname")


class TestPanelsRegistered:
  EXPECTED_PANELS = [
    "VIEW3D_PT_cc_toolkit",
    "VIEW3D_PT_cc_toolkit_crop_canvas",
  ]

  @pytest.mark.parametrize("panel_name", EXPECTED_PANELS)
  def test_panel_exists(self, addon, panel_name):
    assert hasattr(addon, panel_name)
    cls = getattr(addon, panel_name)
    assert hasattr(cls, "bl_label")
