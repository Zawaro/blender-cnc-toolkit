# Tasks

## 1. Baseline specs (already drafted in this change)

- [x] 1.1 Verify `specs/addon-lifecycle/spec.md` against `__init__.py` in all three variants
- [x] 1.2 Verify `specs/game-config/spec.md` against `properties.py` and `GAME_CONFIGS` / `get_config` / `ENGINE_MAP` / `RENDER_TYPE_VIS`
- [x] 1.3 Verify `specs/template-lifecycle/spec.md` against the generate/purge operators and `save_scene_state` / `restore_scene_state` / `clear_template` / `rebuild_all`
- [x] 1.4 Verify `specs/scene-construction/spec.md` against `create_collections` / `create_camera` / `create_light` / `create_world` / `create_planes` / `apply_boolean_modifier`
- [x] 1.5 Verify `specs/render-type-visibility/spec.md` against `RENDER_TYPE_VIS` and `apply_render_type_visibility`
- [x] 1.6 Verify `specs/compositor/spec.md` against `create_compositor` and each `_wire_*` function
- [x] 1.7 Verify `specs/material-remapping/spec.md` against the remap operators and `_create_remap_hue` / Cryptomatte setup
- [x] 1.8 Verify `specs/rendering/spec.md` against the render operators, batch queue, cancel, and `apply_render_settings` shadow filter handling
- [x] 1.9 Verify `specs/crop-canvas/spec.md` against `crop_canvas.py` (code only — no tests)
- [x] 1.10 Verify `specs/variant-compatibility/spec.md` against the three variants' differences (code only — no tests)
- [x] 1.11 Verify `specs/distribution/spec.md` against `dist.py` (code only — no tests)

## 2. Glossary alignment

- [x] 2.1 Confirm every domain term used in the specs appears in `GLOSSARY.md` or is added
- [x] 2.2 Resolve any `Undecided` term the specs depend on before finalizing wording
- [x] 2.3 Add a `Purpose` line to each archived spec referencing its glossary terms

## 3. Flagged quirks (spec recorded as-is, review for follow-up)

- [x] 3.1 Flag the Default render type showing only the grey plane despite its `RENDER_TYPE_VIS["DEFAULT"]` naming
- [x] 3.2 Flag the Shadow matte target differing between Cycles and Eevee
- [x] 3.3 Flag the Cycles-only sun hiding and Cycles-only shadow catcher in CyclesX
- [x] 3.4 Open a follow-up issue for any quirk the maintainer judges to be a bug, rather than editing the baseline
  - Filed #50 (GUIDE.md vs `RENDER_TYPE_VIS`). 3.2 judged intentional (Eevee shadow-catcher workaround); 3.3 recorded, not judged.

## 4. Validation and archive

- [x] 4.1 Run `openspec validate --change capture-baseline-specs` and fix all errors
- [x] 4.2 Confirm `hi_five/`, `eevee_next/`, and `cyclesx/` source files are unmodified
- [x] 4.3 Archive the change so `openspec/specs/<capability>/spec.md` is created for all 11 capabilities
- [x] 4.4 Replace the "TBD" Purpose section in each of the 11 archived specs
- [x] 4.5 Run `openspec spec list` and `openspec validate --specs` to confirm the baseline is valid
