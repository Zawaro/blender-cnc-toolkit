import pytest


class TestApplyInitialSettings:
  def test_sets_fps(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    scene_builder.apply_initial_settings(scene_with_addon, props)
    assert scene_with_addon.scene.render.fps == 10

  def test_sets_file_format(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    scene_builder.apply_initial_settings(scene_with_addon, props)
    assert scene_with_addon.scene.render.image_settings.file_format == "PNG"

  def test_sets_filter_size(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    scene_builder.apply_initial_settings(scene_with_addon, props)
    assert scene_with_addon.scene.render.filter_size == pytest.approx(0.7, abs=1e-3)

  def test_sets_cycles_samples(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    props.engine = "CYCLES"
    config = scene_builder.get_config(props.game, props.variant)
    scene_builder.apply_initial_settings(scene_with_addon, props)
    assert scene_with_addon.scene.cycles.samples == config.cycles_samples

  def test_sets_cycles_filter_width(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    props.engine = "CYCLES"
    scene_builder.apply_initial_settings(scene_with_addon, props)
    assert scene_with_addon.scene.cycles.filter_width == pytest.approx(0.8, abs=1e-3)

  def test_resets_shadow_filter_flag(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    props.is_shadow_filter_saved = True
    scene_builder.apply_initial_settings(scene_with_addon, props)
    assert props.is_shadow_filter_saved is False


class TestApplyRenderSettings:
  def test_sets_resolution(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    props.game = "RW"
    props.variant = "BASE"
    scene_builder.apply_render_settings(scene_with_addon, props)
    assert scene_with_addon.scene.render.resolution_x == 1280
    assert scene_with_addon.scene.render.resolution_y == 960

  def test_shadow_saves_filter(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    props.engine = "CYCLES"
    props.render_type = "DEFAULT"
    scene_with_addon.scene.render.filter_size = 2.0
    scene_with_addon.scene.cycles.filter_width = 1.5

    props.render_type = "SHADOW"
    scene_builder.apply_render_settings(scene_with_addon, props)

    assert props.saved_filter_size == 2.0
    assert props.saved_filter_width == 1.5
    assert props.is_shadow_filter_saved is True

  def test_shadow_overrides_filter(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    props.engine = "CYCLES"
    props.render_type = "DEFAULT"
    scene_with_addon.scene.render.filter_size = 2.0
    scene_with_addon.scene.cycles.filter_width = 1.5

    props.render_type = "SHADOW"
    scene_builder.apply_render_settings(scene_with_addon, props)

    assert scene_with_addon.scene.render.filter_size == pytest.approx(0.01, abs=1e-3)
    assert scene_with_addon.scene.cycles.filter_width == pytest.approx(0.01, abs=1e-3)

  def test_non_shadow_restores_filter(self, scene_with_addon, scene_builder):
    props = scene_with_addon.scene.cc_toolkit
    props.engine = "CYCLES"
    props.render_type = "DEFAULT"
    scene_with_addon.scene.render.filter_size = 2.0
    scene_with_addon.scene.cycles.filter_width = 1.5

    props.render_type = "SHADOW"
    scene_builder.apply_render_settings(scene_with_addon, props)

    props.render_type = "DEFAULT"
    scene_builder.apply_render_settings(scene_with_addon, props)

    assert scene_with_addon.scene.render.filter_size == 2.0
    assert scene_with_addon.scene.cycles.filter_width == 1.5
    assert props.is_shadow_filter_saved is False
