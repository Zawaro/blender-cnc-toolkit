import importlib

import bpy
import pytest


@pytest.fixture(scope="module")
def scene_builder(addon_name):
  return importlib.import_module(f"{addon_name}.scene_builder")


@pytest.fixture(scope="function")
def planes_and_sun(scene_with_addon, addon_name):
  """Create test plane objects and a sun for visibility testing."""
  addon = importlib.import_module(addon_name)
  PREFIX = addon.scene_builder.PREFIX
  COLLECTION_NAME = addon.scene_builder.COLLECTION_NAME

  toolkit_coll = bpy.data.collections.new(COLLECTION_NAME)
  bpy.context.scene.collection.children.link(toolkit_coll)

  holdout_coll = bpy.data.collections.new(f"{COLLECTION_NAME} Holdout")
  toolkit_coll.children.link(holdout_coll)

  planes = {}
  for plane_id in (
    "holdout",
    "holdout2",
    "shadow",
    "shadow2",
    "blue",
    "grey",
    "ambient",
  ):
    mesh = bpy.data.meshes.new(f"TestMesh.{plane_id}")
    obj = bpy.data.objects.new(f"{PREFIX}Plane.{plane_id}", mesh)
    holdout_coll.objects.link(obj)
    planes[plane_id] = obj

  light = bpy.data.lights.new("TestLight", "SUN")
  sun = bpy.data.objects.new(f"{PREFIX}Sun", light)
  toolkit_coll.objects.link(sun)

  return planes, sun


class TestRenderTypeVisibility:
  EXPECTED_VIS = {
    "DEFAULT": {
      "holdout": 1,
      "holdout2": 1,
      "shadow": 1,
      "shadow2": 1,
      "blue": 1,
      "grey": 0,
      "ambient": 1,
    },
    "PREVIEW": {
      "holdout": 0,
      "holdout2": 1,
      "shadow": 0,
      "shadow2": 1,
      "blue": 1,
      "grey": 1,
      "ambient": 1,
    },
    "OBJECT": {
      "holdout": 1,
      "holdout2": 1,
      "shadow": 1,
      "shadow2": 1,
      "blue": 1,
      "grey": 1,
      "ambient": 0,
    },
    "BUILDUP": {
      "holdout": 1,
      "holdout2": 0,
      "shadow": 1,
      "shadow2": 1,
      "blue": 1,
      "grey": 1,
      "ambient": 1,
    },
    "SHADOW": {
      "holdout": 0,
      "holdout2": 1,
      "shadow": 0,
      "shadow2": 1,
      "blue": 1,
      "grey": 1,
      "ambient": 1,
    },
  }

  @pytest.mark.parametrize(
    "render_type", ["DEFAULT", "PREVIEW", "OBJECT", "BUILDUP", "SHADOW"]
  )
  def test_plane_visibility(
    self, scene_with_addon, scene_builder, planes_and_sun, render_type
  ):
    planes, sun = planes_and_sun
    scene_with_addon.scene.cc_toolkit.render_type = render_type
    scene_builder.apply_render_type_visibility(scene_with_addon)

    expected = self.EXPECTED_VIS[render_type]
    for plane_id, expected_hide in expected.items():
      obj = planes[plane_id]
      actual_hide = int(obj.hide_render)
      assert actual_hide == expected_hide, (
        f"{render_type}.{plane_id}: expected hide_render={expected_hide}, got {actual_hide}"
      )

  def test_sun_visibility_cycles(self, scene_with_addon, scene_builder, planes_and_sun):
    planes, sun = planes_and_sun
    scene_with_addon.scene.cc_toolkit.engine = "CYCLES"
    scene_builder.apply_render_type_visibility(scene_with_addon)
    assert sun.hide_render is True

  def test_sun_visibility_eevee(self, scene_with_addon, scene_builder, planes_and_sun):
    planes, sun = planes_and_sun
    scene_with_addon.scene.cc_toolkit.engine = "EEVEE"
    scene_with_addon.scene.cc_toolkit.render_type = "DEFAULT"
    scene_builder.apply_render_type_visibility(scene_with_addon)
    assert sun.hide_render is False

  def test_default_render_type_uses_object_visibility(
    self, scene_with_addon, scene_builder, planes_and_sun
  ):
    planes, sun = planes_and_sun
    scene_with_addon.scene.cc_toolkit.render_type = "DEFAULT"
    scene_builder.apply_render_type_visibility(scene_with_addon)

    expected = self.EXPECTED_VIS["DEFAULT"]
    for plane_id, expected_hide in expected.items():
      obj = planes[plane_id]
      actual_hide = int(obj.hide_render)
      assert actual_hide == expected_hide, (
        f"DEFAULT.{plane_id}: expected hide_render={expected_hide}, got {actual_hide}"
      )
