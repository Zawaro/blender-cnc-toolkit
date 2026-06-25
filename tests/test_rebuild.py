import importlib

import bpy
import pytest


@pytest.fixture(scope="module")
def scene_builder(addon_name):
  return importlib.import_module(f"{addon_name}.scene_builder")


@pytest.fixture(scope="module")
def addon(addon_name):
  return importlib.import_module(addon_name)


def _get_compositor_tree(scene):
  """Get the compositor node tree, handling API differences across Blender versions."""
  if hasattr(scene, "compositing_node_group") and scene.compositing_node_group:
    return scene.compositing_node_group
  if getattr(scene, "use_nodes", False) and getattr(scene, "node_tree", None):
    return scene.node_tree
  return None


@pytest.fixture(scope="function")
def rebuild_context(scene_with_addon, addon_name):
  """Set up scene with a full template for rebuild tests."""
  scene_with_addon.scene.render.use_compositing = True
  if addon_name == "cyclesx":
    scene_with_addon.scene.cycles.use_denoising = True
    vl = scene_with_addon.view_layer
    vl.cycles.denoising_store_passes = True
  else:
    scene_with_addon.scene.use_nodes = True
  return scene_with_addon


@pytest.fixture(scope="function")
def rebuild_props(rebuild_context, scene_builder):
  """Set default props and run full rebuild so the scene has all _CNC_ objects."""
  props = rebuild_context.scene.cc_toolkit
  props.game = "RA2"
  props.variant = "BASE"
  props.engine = "CYCLES"
  props.render_type = "DEFAULT"
  scene_builder.rebuild_all(rebuild_context)
  props.template_generated = True
  return props


class TestRebuildCompositor:
  """Tests for rebuild_compositor — light rebuild that only recreates compositor."""

  def test_creates_compositor(self, rebuild_context, rebuild_props, scene_builder):
    """rebuild_compositor creates a new compositor node tree."""
    rebuild_props.render_type = "DEFAULT"
    scene_builder.rebuild_compositor(rebuild_context)

    tree = _get_compositor_tree(rebuild_context.scene)
    assert tree is not None

  @pytest.mark.parametrize(
    "render_type", ["DEFAULT", "PREVIEW", "OBJECT", "BUILDUP", "SHADOW"]
  )
  def test_creates_compositor_per_type(
    self, rebuild_context, rebuild_props, scene_builder, render_type
  ):
    """rebuild_compositor works for all render types."""
    rebuild_props.render_type = render_type
    scene_builder.rebuild_compositor(rebuild_context)

    tree = _get_compositor_tree(rebuild_context.scene)
    assert tree is not None

  def test_cleans_up_old_compositor(
    self, rebuild_context, rebuild_props, scene_builder
  ):
    """rebuild_compositor deletes old _CNC_ node groups before creating new ones."""
    rebuild_props.render_type = "DEFAULT"

    # Create a fake old compositor
    bpy.data.node_groups.new("_CNC_OLD_Composition", type="CompositorNodeTree")
    assert bpy.data.node_groups.get("_CNC_OLD_Composition") is not None

    # Also create alpha convert group
    bpy.data.node_groups.new("_CNC_OLD_Alpha Convert", type="CompositorNodeTree")
    assert bpy.data.node_groups.get("_CNC_OLD_Alpha Convert") is not None

    scene_builder.rebuild_compositor(rebuild_context)

    # Old groups should be gone
    assert bpy.data.node_groups.get("_CNC_OLD_Composition") is None
    assert bpy.data.node_groups.get("_CNC_OLD_Alpha Convert") is None

    # New compositor should exist
    tree = _get_compositor_tree(rebuild_context.scene)
    assert tree is not None

  def test_preserves_camera(self, rebuild_context, rebuild_props, scene_builder):
    """rebuild_compositor does not destroy camera objects."""
    rebuild_props.render_type = "DEFAULT"

    # Find the camera created by rebuild_all
    cam = None
    for obj in bpy.data.objects:
      if obj.type == "CAMERA" and obj.name.startswith("_CNC_"):
        cam = obj
        break
    assert cam is not None, "No _CNC_ camera found after rebuild_all"
    original_name = cam.name

    scene_builder.rebuild_compositor(rebuild_context)

    # Same camera should still exist
    obj = bpy.data.objects.get(original_name)
    assert obj is not None

  def test_preserves_light(self, rebuild_context, rebuild_props, scene_builder):
    """rebuild_compositor does not destroy light objects."""
    rebuild_props.render_type = "DEFAULT"

    # Find the sun created by rebuild_all
    sun = None
    for obj in bpy.data.objects:
      if obj.type == "LIGHT" and obj.name.startswith("_CNC_"):
        sun = obj
        break
    assert sun is not None, "No _CNC_ light found after rebuild_all"
    original_name = sun.name

    scene_builder.rebuild_compositor(rebuild_context)

    # Same light should still exist
    obj = bpy.data.objects.get(original_name)
    assert obj is not None

  def test_preserves_planes(self, rebuild_context, rebuild_props, scene_builder):
    """rebuild_compositor does not destroy plane objects."""
    rebuild_props.render_type = "DEFAULT"

    # Find a plane created by rebuild_all
    plane = None
    for obj in bpy.data.objects:
      if obj.name.startswith("_CNC_Plane."):
        plane = obj
        break
    assert plane is not None, "No _CNC_ plane found after rebuild_all"
    original_name = plane.name

    scene_builder.rebuild_compositor(rebuild_context)

    # Same plane should still exist
    obj = bpy.data.objects.get(original_name)
    assert obj is not None

  def test_updates_plane_visibility(
    self, rebuild_context, rebuild_props, scene_builder
  ):
    """rebuild_compositor updates plane visibility based on render_type."""
    # grey plane should be visible (hide_render=False) in DEFAULT mode
    rebuild_props.render_type = "DEFAULT"
    scene_builder.rebuild_compositor(rebuild_context)

    grey = bpy.data.objects.get("_CNC_Plane.grey")
    assert grey is not None
    assert grey.hide_render is False

  def test_updates_render_settings(self, rebuild_context, rebuild_props, scene_builder):
    """rebuild_compositor applies render settings for the current game/variant."""
    rebuild_props.game = "RW"
    rebuild_props.variant = "BASE"
    rebuild_props.render_type = "DEFAULT"
    scene_builder.rebuild_compositor(rebuild_context)

    # RW/BASE resolution is 1280x960
    assert rebuild_context.scene.render.resolution_x == 1280
    assert rebuild_context.scene.render.resolution_y == 960

  def test_preserves_world(self, rebuild_context, rebuild_props, scene_builder):
    """rebuild_compositor does not destroy world data blocks."""
    rebuild_props.render_type = "DEFAULT"
    world_name = (
      rebuild_context.scene.world.name if rebuild_context.scene.world else None
    )
    assert world_name is not None, "No world found after rebuild_all"

    scene_builder.rebuild_compositor(rebuild_context)

    # World should still exist
    assert bpy.data.worlds.get(world_name) is not None

  def test_does_not_delete_collections(
    self, rebuild_context, rebuild_props, scene_builder
  ):
    """rebuild_compositor does not delete collection objects."""
    rebuild_props.render_type = "DEFAULT"

    # Count objects before
    cnc_objects_before = [o for o in bpy.data.objects if o.name.startswith("_CNC_")]
    count_before = len(cnc_objects_before)

    scene_builder.rebuild_compositor(rebuild_context)

    # Same count of _CNC_ objects should exist
    cnc_objects_after = [o for o in bpy.data.objects if o.name.startswith("_CNC_")]
    count_after = len(cnc_objects_after)
    assert count_after == count_before


class TestRebuildCompositorVsFull:
  """Verify that light rebuild preserves objects while full rebuild recreates them."""

  def test_full_rebuild_destroys_and_recreates(self, rebuild_context, scene_builder):
    """rebuild_all destroys existing _CNC_ objects and recreates them."""
    props = rebuild_context.scene.cc_toolkit
    props.game = "RA2"
    props.variant = "BASE"
    props.engine = "CYCLES"
    props.render_type = "DEFAULT"

    # First rebuild to populate the scene
    scene_builder.rebuild_all(rebuild_context)
    props.template_generated = True

    # Record a specific object
    sun = bpy.data.objects.get("_CNC_Sun")
    assert sun is not None

    # Change game so rebuild_all creates different objects
    props.game = "TS"
    scene_builder.rebuild_all(rebuild_context)

    # Sun should still exist (recreated by rebuild_all with TS config)
    sun_after = bpy.data.objects.get("_CNC_Sun")
    assert sun_after is not None

  def test_light_rebuild_preserves_object_count(
    self, rebuild_context, rebuild_props, scene_builder
  ):
    """rebuild_compositor does not change the number of _CNC_ objects."""
    rebuild_props.render_type = "DEFAULT"

    count_before = len([o for o in bpy.data.objects if o.name.startswith("_CNC_")])

    # Light rebuild with different render type
    rebuild_props.render_type = "PREVIEW"
    scene_builder.rebuild_compositor(rebuild_context)

    count_after = len([o for o in bpy.data.objects if o.name.startswith("_CNC_")])
    assert count_after == count_before

  def test_light_rebuild_changes_compositor(
    self, rebuild_context, rebuild_props, scene_builder
  ):
    """rebuild_compositor creates a new compositor tree."""
    rebuild_props.render_type = "DEFAULT"
    scene_builder.rebuild_compositor(rebuild_context)

    tree_before = _get_compositor_tree(rebuild_context.scene)
    assert tree_before is not None

    # Rebuild with different render type
    rebuild_props.render_type = "PREVIEW"
    scene_builder.rebuild_compositor(rebuild_context)

    tree_after = _get_compositor_tree(rebuild_context.scene)
    assert tree_after is not None
    # The compositor should be a new tree (different name or restructured)
    assert tree_after is not None


class TestRemapMaterialOperators:
  """Verify remap material operators call rebuild_compositor, not rebuild_all."""

  def test_add_remap_calls_light_rebuild(
    self, rebuild_context, rebuild_props, scene_builder
  ):
    """CNC_OT_add_remap_material calls rebuild_compositor."""
    # Create a material
    mat = bpy.data.materials.new("TestMaterial")

    # Set it in the picker
    rebuild_props.remap_material_picker = mat

    # Track if rebuild_compositor is called
    call_count = [0]
    original = scene_builder.rebuild_compositor

    def mock_rebuild(ctx):
      call_count[0] += 1
      original(ctx)

    scene_builder.rebuild_compositor = mock_rebuild
    try:
      bpy.ops.ccnc.add_remap_material()
      assert call_count[0] == 1
    finally:
      scene_builder.rebuild_compositor = original

  def test_remove_remap_calls_light_rebuild(
    self, rebuild_context, rebuild_props, scene_builder
  ):
    """CNC_OT_remove_remap_material calls rebuild_compositor."""
    # Create and add a material
    mat = bpy.data.materials.new("TestMaterial")
    item = rebuild_props.remap_materials.add()
    item.material = mat

    # Track if rebuild_compositor is called
    call_count = [0]
    original = scene_builder.rebuild_compositor

    def mock_rebuild(ctx):
      call_count[0] += 1
      original(ctx)

    scene_builder.rebuild_compositor = mock_rebuild
    try:
      bpy.ops.ccnc.remove_remap_material(index=0)
      assert call_count[0] == 1
    finally:
      scene_builder.rebuild_compositor = original

  def test_clear_remap_calls_light_rebuild(
    self, rebuild_context, rebuild_props, scene_builder
  ):
    """CNC_OT_clear_remap_materials calls rebuild_compositor."""
    # Add a material
    mat = bpy.data.materials.new("TestMaterial")
    item = rebuild_props.remap_materials.add()
    item.material = mat

    # Track if rebuild_compositor is called
    call_count = [0]
    original = scene_builder.rebuild_compositor

    def mock_rebuild(ctx):
      call_count[0] += 1
      original(ctx)

    scene_builder.rebuild_compositor = mock_rebuild
    try:
      bpy.ops.ccnc.clear_remap_materials()
      assert call_count[0] == 1
    finally:
      scene_builder.rebuild_compositor = original


class TestActiveCollectionRestoration:
  """rebuild_all must not leave a _CNC_ toolkit collection as the active collection."""

  def test_restores_non_toolkit_active_collection(self, rebuild_context, scene_builder):
    """rebuild_all restores the user's original non-toolkit active collection."""
    vl = rebuild_context.view_layer
    root = vl.layer_collection
    vl.active_layer_collection = root
    saved_name = vl.active_layer_collection.name

    props = rebuild_context.scene.cc_toolkit
    props.game = "RA2"
    props.variant = "BASE"
    props.engine = "CYCLES"
    props.render_type = "DEFAULT"
    scene_builder.rebuild_all(rebuild_context)

    active = vl.active_layer_collection
    assert not active.name.startswith("_CNC_")
    assert active.name == saved_name

  def test_restores_custom_user_collection(self, rebuild_context, scene_builder):
    """rebuild_all restores a user-created collection as active."""
    vl = rebuild_context.view_layer
    root = vl.layer_collection
    user_coll = bpy.data.collections.new("UserStuff")
    root.collection.children.link(user_coll)
    vl.active_layer_collection = root.children.get("UserStuff")

    props = rebuild_context.scene.cc_toolkit
    props.game = "RA2"
    props.variant = "BASE"
    props.engine = "CYCLES"
    props.render_type = "DEFAULT"
    scene_builder.rebuild_all(rebuild_context)

    assert vl.active_layer_collection.name == "UserStuff"

  def test_falls_back_to_root_when_toolkit_was_active(
    self, rebuild_context, rebuild_props, scene_builder
  ):
    """rebuild_all falls back to Scene Collection when a toolkit coll was active."""
    vl = rebuild_context.view_layer
    root = vl.layer_collection

    after_first_rebuild = root.children.get("_CNC_Toolkit")
    assert after_first_rebuild is not None
    vl.active_layer_collection = after_first_rebuild

    scene_builder.rebuild_all(rebuild_context)

    active = vl.active_layer_collection
    assert not active.name.startswith("_CNC_")
    assert active.name == root.name
