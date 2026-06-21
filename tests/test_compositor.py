import importlib

import bpy
import pytest


@pytest.fixture(scope="module")
def scene_builder(addon_name):
  return importlib.import_module(f"{addon_name}.scene_builder")


def _get_compositor_tree(scene):
  """Get the compositor node tree, handling API differences across Blender versions."""
  if hasattr(scene, "compositing_node_group") and scene.compositing_node_group:
    return scene.compositing_node_group
  if getattr(scene, "use_nodes", False) and getattr(scene, "node_tree", None):
    return scene.node_tree
  return None


@pytest.fixture(scope="function")
def compositor_context(scene_with_addon, addon_name):
  """Ensure compositing is enabled for compositor tests."""
  scene_with_addon.scene.render.use_compositing = True
  if addon_name == "cyclesx":
    scene_with_addon.scene.cycles.use_denoising = True
    vl = scene_with_addon.view_layer
    vl.cycles.denoising_store_passes = True
  else:
    scene_with_addon.scene.use_nodes = True
  return scene_with_addon


@pytest.fixture(scope="function")
def compositor_props(compositor_context):
  """Set default props for compositor tests (RA2/BASE/CYCLES)."""
  props = compositor_context.scene.cc_toolkit
  props.game = "RA2"
  props.variant = "BASE"
  props.engine = "CYCLES"
  return props


class TestCreateCompositor:
  @pytest.mark.parametrize(
    "render_type", ["DEFAULT", "PREVIEW", "OBJECT", "BUILDUP", "SHADOW"]
  )
  def test_creates_node_tree(
    self, compositor_context, compositor_props, scene_builder, render_type
  ):
    compositor_props.render_type = render_type
    scene_builder.create_compositor(compositor_context, compositor_props)

    tree = _get_compositor_tree(compositor_context.scene)
    assert tree is not None

  @pytest.mark.parametrize(
    "render_type", ["DEFAULT", "PREVIEW", "OBJECT", "BUILDUP", "SHADOW"]
  )
  def test_has_render_layer_node(
    self, compositor_context, compositor_props, scene_builder, render_type
  ):
    compositor_props.render_type = render_type
    scene_builder.create_compositor(compositor_context, compositor_props)

    tree = _get_compositor_tree(compositor_context.scene)
    rl_nodes = [n for n in tree.nodes if n.bl_idname == "CompositorNodeRLayers"]
    assert len(rl_nodes) == 1

  @pytest.mark.parametrize(
    "render_type", ["DEFAULT", "PREVIEW", "OBJECT", "BUILDUP", "SHADOW"]
  )
  def test_has_output_node(
    self, compositor_context, compositor_props, scene_builder, render_type
  ):
    compositor_props.render_type = render_type
    scene_builder.create_compositor(compositor_context, compositor_props)

    tree = _get_compositor_tree(compositor_context.scene)
    output_nodes = [
      n
      for n in tree.nodes
      if n.bl_idname in ("NodeGroupOutput", "CompositorNodeComposite")
    ]
    assert len(output_nodes) >= 1

  @pytest.mark.parametrize(
    "render_type", ["DEFAULT", "PREVIEW", "OBJECT", "BUILDUP", "SHADOW"]
  )
  def test_has_links(
    self, compositor_context, compositor_props, scene_builder, render_type
  ):
    compositor_props.render_type = render_type
    scene_builder.create_compositor(compositor_context, compositor_props)

    tree = _get_compositor_tree(compositor_context.scene)
    assert len(tree.links) > 0

  def test_creates_alpha_convert_group(
    self, compositor_context, compositor_props, scene_builder
  ):
    compositor_props.render_type = "DEFAULT"
    scene_builder.create_compositor(compositor_context, compositor_props)

    alpha_group = bpy.data.node_groups.get("_CNC_Alpha Convert")
    assert alpha_group is not None

  def test_default_sets_rgb_color_mode(
    self, compositor_context, compositor_props, scene_builder
  ):
    compositor_props.render_type = "DEFAULT"
    scene_builder.create_compositor(compositor_context, compositor_props)

    assert compositor_context.scene.render.image_settings.color_mode == "RGB"

  def test_default_sets_film_transparent_false(
    self, compositor_context, compositor_props, scene_builder
  ):
    compositor_props.render_type = "DEFAULT"
    scene_builder.create_compositor(compositor_context, compositor_props)

    assert compositor_context.scene.render.film_transparent is False
