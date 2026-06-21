import importlib
import re
from pathlib import Path

try:
  import tomllib
except ModuleNotFoundError:
  import tomli as tomllib

import pytest


@pytest.fixture(scope="module")
def properties(addon_name):
  return importlib.import_module(f"{addon_name}.properties")


@pytest.fixture(scope="module")
def init_module(addon_name):
  return importlib.import_module(addon_name)


class TestEnumItems:
  @staticmethod
  def _extract_values(items):
    return [item[0] for item in items]

  def test_game_items_no_duplicates(self, properties):
    values = self._extract_values(properties.GAME_ITEMS)
    assert len(values) == len(set(values))

  def test_variant_items_no_duplicates(self, properties):
    values = self._extract_values(properties.VARIANT_ITEMS)
    assert len(values) == len(set(values))

  def test_engine_items_no_duplicates(self, properties):
    values = self._extract_values(properties.ENGINE_ITEMS)
    assert len(values) == len(set(values))

  def test_camera_mode_items_no_duplicates(self, properties):
    values = self._extract_values(properties.CAMERA_MODE_ITEMS)
    assert len(values) == len(set(values))

  def test_render_type_items_no_duplicates(self, properties):
    values = self._extract_values(properties.RENDER_TYPE_ITEMS)
    assert len(values) == len(set(values))

  def test_game_items_has_expected_count(self, properties):
    assert len(properties.GAME_ITEMS) == 6

  def test_variant_items_has_expected_count(self, properties):
    assert len(properties.VARIANT_ITEMS) == 3

  def test_engine_items_has_expected_count(self, properties):
    assert len(properties.ENGINE_ITEMS) == 2

  def test_render_type_items_has_expected_count(self, properties):
    assert len(properties.RENDER_TYPE_ITEMS) == 5


class TestVersionString:
  def test_format(self, init_module):
    match = re.match(r"^\d+\.\d+\.\d+ \(build \d+\)$", init_module.VERSION_STRING)
    assert match, (
      f"VERSION_STRING '{init_module.VERSION_STRING}' doesn't match expected format"
    )

  def test_version_matches_bl_info(self, init_module):
    version_tuple = init_module.bl_info["version"]
    expected = ".".join(str(v) for v in version_tuple)
    assert init_module.VERSION_STRING.startswith(expected)

  def test_bl_info_has_required_keys(self, init_module):
    required = {
      "name",
      "author",
      "version",
      "blender",
      "location",
      "description",
      "category",
    }
    assert required.issubset(set(init_module.bl_info.keys()))


class TestManifestVersion:
  def test_manifest_version_matches_bl_info(self, addon_name, init_module):
    manifest_path = Path(__file__).parent.parent / addon_name / "blender_manifest.toml"
    with open(manifest_path, "rb") as f:
      manifest = tomllib.load(f)
    bl_info_version = ".".join(str(v) for v in init_module.bl_info["version"])
    assert manifest["version"] == bl_info_version
