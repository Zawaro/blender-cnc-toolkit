import importlib

import pytest


@pytest.fixture(scope="module")
def scene_builder(addon_name):
  return importlib.import_module(f"{addon_name}.scene_builder")


class TestEngineMap:
  def test_has_cycles(self, scene_builder):
    assert "CYCLES" in scene_builder.ENGINE_MAP

  def test_has_eevee(self, scene_builder):
    assert "EEVEE" in scene_builder.ENGINE_MAP

  def test_cycles_maps_to_cycles(self, scene_builder):
    assert scene_builder.ENGINE_MAP["CYCLES"] == "CYCLES"

  def test_eevee_maps_to_blender_engine(self, scene_builder):
    val = scene_builder.ENGINE_MAP["EEVEE"]
    assert val in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT")


class TestGameConfigs:
  EXPECTED_GAMES = {"RA2", "TS", "RW", "RA1", "RM", "D2K"}
  EXPECTED_VARIANTS = {"BASE", "INF", "FX"}

  def test_has_all_games(self, scene_builder):
    assert set(scene_builder.GAME_CONFIGS.keys()) == self.EXPECTED_GAMES

  @pytest.mark.parametrize("game", ["RA2", "TS", "RW", "RA1", "RM", "D2K"])
  def test_game_has_all_variants(self, scene_builder, game):
    assert set(scene_builder.GAME_CONFIGS[game].keys()) == self.EXPECTED_VARIANTS

  @pytest.mark.parametrize("game", ["RA2", "TS", "RW", "RA1", "RM", "D2K"])
  def test_variant_has_resolution(self, scene_builder, game):
    for variant in ("BASE", "INF", "FX"):
      cfg = scene_builder.GAME_CONFIGS[game][variant]
      assert hasattr(cfg, "resolution")
      assert isinstance(cfg.resolution, tuple)
      assert len(cfg.resolution) == 2

  def test_ra2_inf_override(self, scene_builder):
    cfg = scene_builder.GAME_CONFIGS["RA2"]["INF"]
    assert cfg.resolution == (320, 240)
    assert cfg.camera_ortho_scale == 14.96

  def test_ts_base_override(self, scene_builder):
    cfg = scene_builder.GAME_CONFIGS["TS"]["BASE"]
    assert cfg.camera_ortho_scale == 37.4
    assert cfg.sun_energy in (4, 5)  # 4=cyclesx, 5=hi_five/eevee_next

  def test_rw_base_override(self, scene_builder):
    cfg = scene_builder.GAME_CONFIGS["RW"]["BASE"]
    assert cfg.resolution == (1280, 960)
    assert cfg.sun_energy in (6.5, 7.5)  # 6.5=cyclesx, 7.5=hi_five/eevee_next

  @pytest.mark.parametrize("game", ["RA2", "TS", "RW", "RA1", "RM", "D2K"])
  def test_inf_inherits_base_when_no_override(self, scene_builder, game):
    base = scene_builder.GAME_CONFIGS[game]["BASE"]
    inf = scene_builder.GAME_CONFIGS[game]["INF"]
    if game not in ("RA2", "TS"):
      assert inf.resolution == base.resolution
      assert inf.camera_ortho_scale == base.camera_ortho_scale


class TestGetConfig:
  def test_known_game_known_variant(self, scene_builder):
    cfg = scene_builder.get_config("RA2", "BASE")
    assert cfg is scene_builder.GAME_CONFIGS["RA2"]["BASE"]

  def test_known_game_unknown_variant_fallback(self, scene_builder):
    cfg = scene_builder.get_config("RA2", "NONEXISTENT")
    assert cfg is scene_builder.GAME_CONFIGS["RA2"]["BASE"]

  def test_unknown_game_fallback(self, scene_builder):
    cfg = scene_builder.get_config("BOGUS", "BASE")
    assert cfg is scene_builder.GAME_CONFIGS["RA2"]["BASE"]

  def test_unknown_game_unknown_variant_fallback(self, scene_builder):
    cfg = scene_builder.get_config("BOGUS", "NONEXISTENT")
    assert cfg is scene_builder.GAME_CONFIGS["RA2"]["BASE"]


class TestRenderTypeVis:
  EXPECTED_TYPES = {"DEFAULT", "PREVIEW", "OBJECT", "BUILDUP", "SHADOW"}
  EXPECTED_PLANES = {
    "holdout",
    "holdout2",
    "shadow",
    "shadow2",
    "blue",
    "grey",
    "ambient",
  }

  def test_has_all_types(self, scene_builder):
    assert set(scene_builder.RENDER_TYPE_VIS.keys()) == self.EXPECTED_TYPES

  @pytest.mark.parametrize(
    "render_type", ["DEFAULT", "PREVIEW", "OBJECT", "BUILDUP", "SHADOW"]
  )
  def test_type_has_all_planes(self, scene_builder, render_type):
    planes = set(scene_builder.RENDER_TYPE_VIS[render_type].keys())
    assert planes == self.EXPECTED_PLANES

  @pytest.mark.parametrize(
    "render_type", ["DEFAULT", "PREVIEW", "OBJECT", "BUILDUP", "SHADOW"]
  )
  def test_plane_values_are_zero_or_one(self, scene_builder, render_type):
    for plane, val in scene_builder.RENDER_TYPE_VIS[render_type].items():
      assert val in (0, 1), f"{render_type}.{plane} = {val}, expected 0 or 1"
