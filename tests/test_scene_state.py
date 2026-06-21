import importlib
import json

import bpy
import pytest


@pytest.fixture(scope="module")
def scene_builder(addon_name):
  return importlib.import_module(f"{addon_name}.scene_builder")


class TestSaveRestoreRoundtrip:
  def test_save_creates_json(self, scene_with_addon, scene_builder):
    scene = scene_with_addon.scene
    scene_builder.save_scene_state(scene_with_addon)
    saved = scene.cc_toolkit.saved_state
    assert saved
    state = json.loads(saved)
    assert "resolution_x" in state
    assert "engine" in state

  def test_roundtrip_preserves_values(self, scene_with_addon, scene_builder):
    scene = scene_with_addon.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.fps = 30
    scene_builder.save_scene_state(scene_with_addon)

    scene.render.resolution_x = 640
    scene.render.resolution_y = 480
    scene.render.fps = 24

    scene_builder.restore_scene_state(scene_with_addon)
    assert scene.render.resolution_x == 1920
    assert scene.render.resolution_y == 1080
    assert scene.render.fps == 30

  def test_restore_empty_state_no_crash(self, scene_with_addon, scene_builder):
    scene = scene_with_addon.scene
    scene.cc_toolkit.saved_state = ""
    scene_builder.restore_scene_state(scene_with_addon)

  def test_restore_invalid_json_no_crash(self, scene_with_addon, scene_builder):
    scene = scene_with_addon.scene
    scene.render.resolution_x = 999
    scene.cc_toolkit.saved_state = "not valid json"
    try:
      scene_builder.restore_scene_state(scene_with_addon)
    except json.JSONDecodeError:
      pass
    assert scene.render.resolution_x == 999

  def test_restore_deleted_world_no_crash(self, scene_with_addon, scene_builder):
    scene = scene_with_addon.scene
    world = bpy.data.worlds.new("TestWorld")
    scene.world = world
    scene_builder.save_scene_state(scene_with_addon)

    bpy.data.worlds.remove(world)
    scene_builder.restore_scene_state(scene_with_addon)

  def test_restore_deleted_compositor_no_crash(self, scene_with_addon, scene_builder):
    scene = scene_with_addon.scene
    tree = bpy.data.node_groups.new("TestCompositor", type="CompositorNodeTree")
    if hasattr(scene, "compositing_node_group"):
      scene.compositing_node_group = tree
    else:
      scene.use_nodes = True
    scene_builder.save_scene_state(scene_with_addon)

    bpy.data.node_groups.remove(tree)
    scene_builder.restore_scene_state(scene_with_addon)


class TestFilterWidthRestore:
  def test_filter_width_restored_for_cycles(self, scene_with_addon, scene_builder):
    scene = scene_with_addon.scene
    scene.render.engine = "CYCLES"
    scene.cycles.filter_width = 1.5
    scene_builder.save_scene_state(scene_with_addon)

    scene.cycles.filter_width = 0.1
    scene_builder.restore_scene_state(scene_with_addon)
    assert scene.cycles.filter_width == 1.5

  def test_filter_size_restored(self, scene_with_addon, scene_builder):
    scene = scene_with_addon.scene
    scene.render.filter_size = 2.5
    scene_builder.save_scene_state(scene_with_addon)

    scene.render.filter_size = 0.1
    scene_builder.restore_scene_state(scene_with_addon)
    assert scene.render.filter_size == 2.5
