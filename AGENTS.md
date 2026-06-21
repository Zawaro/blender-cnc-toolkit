# Blender C&C Toolkit — Agent Guide

## Project structure

Three addon variants in separate directories, each a self-contained Blender addon:

- `hi_five/` — Blender 5.0+ (primary)
- `eevee_next/` — Blender 4.2–4.x
- `cyclesx/` — Blender 3.0–3.6

Each variant shares the same file layout: `__init__.py`, `scene_builder.py`, `operators.py`, `properties.py`, `panel.py`, `crop_canvas.py`, `node_arrange.py`, `assets/`, and `blender_manifest.toml` (hi_five and eevee_next only).

`dist.py` builds versioned `.zip` files to `.dist/`. Build number comes from `git rev-list --count HEAD`.

## Variant differences (the stuff that trips you up)

**hi_five vs eevee_next** — nearly identical code with these differences:
- `ENGINE_MAP`: `"EEVEE"` maps to `BLENDER_EEVEE` (hi_five) vs `BLENDER_EEVEE_NEXT` (eevee_next)
- Eevee Next uses `CompositorNodeSepHSVA`/`CompositorNodeCombHSVA` (Blender 4.x API) instead of `CompositorNodeSeparateColor`/`CompositorNodeCombineColor` (Blender 5.x)
- Eevee Next clears compositor by removing nodes from `scene.node_tree` (read-only in 4.3); HiFive sets `scene.compositing_node_group = None`
- Eevee Next sets `world.use_nodes = True` and `material.use_nodes = True` explicitly
- Eevee Next has extra shadow buffer properties and uses `sky.dust_density` / `NISHITA` sky type

**hi_five vs cyclesx** — cyclesx has significantly different scene_builder (~1250 lines vs ~940):
- CyclesX adds Cryptomatte holdout handling (`obj.is_holdout = True` on planes)
- CyclesX has a dedicated denoise panel (`denoise_composite`, `denoise_render` properties)
- CyclesX uses `shadow_catcher` parameter on plane objects
- CyclesX does NOT have `blender_manifest.toml` in the zip (excluded by `dist.py`)

**Never copy code between variants without checking the differences above.**

## Build and dist

```sh
./dist.sh          # interactive: prompts for which variant(s) to build
python dist.py     # same, but requires activated venv
```

- Output: `.dist/<name>_<version>_build<N>.zip`
- Build number = total git commits; version from `bl_info` in `__init__.py`
- `_build.py` is generated during build (gitignored) and included in zip for version display
- `blender_manifest.toml` version must match `bl_info` version in `__init__.py`

## Testing

Uses [pytest-blender](https://github.com/mondeja/pytest-blender) for addon testing. Tests run inside Blender's headless Python interpreter.

```sh
uv sync --group test --group dev          # install all deps
uv run pre-commit install                 # install pre-commit hooks

# Single variant
BLENDER_EXECUTABLE=/path/to/blender ./test.sh

# All variants (set paths in .env first)
cp .env.example .env   # edit with your Blender paths
./test.sh --all

# Or run pytest directly
BLENDER_ADDON=hi_five BLENDER_EXECUTABLE=/path/to/blender uv run pytest --blender-addons-dirs . -v -- -noaudio
```

`.env` maps addon variants to local Blender executables:
- `BLENDER_5` → hi_five (Blender 5.0+)
- `BLENDER_4` → eevee_next (Blender 4.2–4.x)
- `BLENDER_3` → cyclesx (Blender 3.0–3.6)

Each Blender's Python needs pytest installed: `<blender>/python/bin/python3.XX -m pip install pytest`

Test structure:
- `tests/conftest.py` — shared fixtures (`addon_name`, `addon_module`, `clean_scene`, `scene_with_addon`)
- `tests/test_config.py` — GAME_CONFIGS, get_config, ENGINE_MAP, RENDER_TYPE_VIS
- `tests/test_properties.py` — enum item validation, VERSION_STRING, manifest version
- `tests/test_registration.py` — addon registration, operator/panel existence
- `tests/test_scene_state.py` — save/restore scene state round-trips
- `tests/test_visibility.py` — render type visibility per plane/sun
- `tests/test_render.py` — initial settings, render settings, shadow filter save/restore
- `tests/test_compositor.py` — compositor node tree creation per render type

CI runs on PRs to main via `.github/workflows/test.yml` (lint + 3-variant matrix).

## Blender extension permissions

HiFive and Eevee Next targets Blender 4.2+ extension system. The manifest requires `permissions = ["files"]` to allow `bpy.data.images.load()` to read bundled HDRI textures from the addon directory.

## Code style

- 2-space indent (enforced by ruff config in `pyproject.toml`)
- No docstrings on classes/functions (pylintrc disables C0114/C0115/C0116)
- No module-level docstrings either (C0103 disabled)
- `from __future__ import annotations` at top of `scene_builder.py`

## Versioning

Version lives in two places that must stay in sync:
- `bl_info["version"]` in `__init__.py` — tuple `(0, 1, 1)`
- `version` in `blender_manifest.toml` — string `"0.1.1"`

When bumping version, update both files in all affected variants.

## Gotchas

- `scene.view_layers["ViewLayer"]` does NOT work in Blender 5.0 (view layer renamed). Use `context.view_layer`.
- `scene.eevee.use_shadows` does NOT exist in Blender 3.0. CyclesX must not set it.
- When changing `render_type`, `background_color`, `shadow_color`, or `shadow_opacity`, use `_rebuild_if_generated` (not `_update_params`) as the property update callback — the compositor needs to be rewired.
- Crop canvas resolution must be refreshed at the end of `rebuild_all()` or it shows stale values.
- User-imported objects outside the `_CNC_Toolkit` collection are preserved during rebuilds.

## GitHub CLI

`gh` is available for issue and PR workflows. Common commands:

- `gh issue create` — file a new issue
- `gh issue list` — list open issues
- `gh pr view` — view a pull request

## Issues

Bugs and feature requests are tracked via GitHub Issues. Use the existing labels:

- `bug` — something isn't working
- `enhancement` — new feature or request
- `documentation` — docs improvements
- `good first issue` — good for newcomers
- `help wanted` — extra attention needed
