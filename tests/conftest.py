import importlib
import os

import pytest


@pytest.fixture(scope="session")
def addon_name():
  """Return the addon module name based on BLENDER_ADDON environment variable."""
  name = os.environ.get("BLENDER_ADDON", "hi_five")
  return name


@pytest.fixture(scope="session")
def addon_module(addon_name):
  """Import the addon module after pytest-blender installs it."""
  return importlib.import_module(addon_name)


@pytest.fixture(scope="function")
def clean_scene():
  """Clear scene objects without resetting addon registrations."""
  import bpy

  scene = bpy.context.scene
  for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
  for coll in list(bpy.data.collections):
    if coll.name != "Collection":
      bpy.data.collections.remove(coll)
  scene.render.engine = "CYCLES"
  scene.render.resolution_x = 640
  scene.render.resolution_y = 480
  scene.frame_start = 1
  scene.frame_end = 250
  yield
  for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)


@pytest.fixture(scope="function")
def scene_with_addon(clean_scene, addon_module):
  """Scene with addon already registered by pytest-blender."""
  import bpy

  assert hasattr(bpy.types.Scene, "cc_toolkit"), "Addon not registered"
  yield bpy.context
