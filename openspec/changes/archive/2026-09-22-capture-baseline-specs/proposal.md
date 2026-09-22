## Why

OpenSpec was just initialized with zero specs, so future changes would propose against
nothing. The addon already works, but its behavior lives only in code, three near-identical
variant copies, and a partial test suite. We need an as-built behavioral baseline so
`openspec/specs/` describes what the toolkit must do today and every future change has a
spec to modify.

## What Changes

- Reverse-engineer the current behavior of all three variants (`hi_five`, `eevee_next`,
  `cyclesx`) into capability specs under `openspec/specs/`.
- Define each capability as behavior-level requirements (WHEN/THEN scenarios), not
  implementation details, using `GLOSSARY.md` terms verbatim.
- Capture the Blender-version and engine differences between the three variants in a
  dedicated `variant-compatibility` capability instead of triplicating every requirement.
- Record known behavioral quirks as-is, with a note flagging any that look like bugs
  rather than intent.
- No runtime code changes: this change only adds specs and the design/tasks around them.

## Capabilities

### New Capabilities

- `addon-lifecycle`: registration and unregistration of classes, scene properties,
  the crop-canvas depsgraph handler, the bundled usage guide, and version reporting across
  `hi_five`, `eevee_next`, `cyclesx`.
- `game-config`: game / variant / engine / camera-mode enums, `GAME_CONFIGS` resolution and
  fallback, `ENGINE_MAP`, and the `RENDER_TYPE_VIS` visibility table.
- `template-lifecycle`: Generate Template and Purge Template, full mutation on parameter
  change, pre-template scene-state save/restore, `_CNC_` data cleanup, and active-collection
  restoration, across all three variants.
- `scene-construction`: creation of collections, camera (with view switch), sun, world
  HDRI/sky, render planes, and the boolean cutter, across all three variants.
- `render-type-visibility`: plane, holdout-collection, and sun visibility per render type,
  across all three variants.
- `compositor`: the Alpha Convert node group, per-render-type compositor wiring, background
  color/image, anti-aliasing, transparent background, shadow tint/opacity, and output color
  mode, across all three variants.
- `material-remapping`: the remap material picker, add/remove/clear operators, remap color,
  Cryptomatte material pass, and compositor rebuild, across all three variants.
- `rendering`: Render Current with frame offset, Render Animation, the Render + Shadow batch
  queue with auto frame offset, user cancellation, and shadow filter save/override, across
  all three variants.
- `crop-canvas`: crop dimensions, centered render border, the self-disabling monitor, and the
  crop panels, across all three variants.
- `variant-compatibility`: the deliberate behavior differences between `hi_five`,
  `eevee_next`, and `cyclesx` — engine mapping, compositor node APIs, compositor clearing,
  world/material `use_nodes`, sky type, Cryptomatte holdout, the denoise panel, and manifest
  packaging.
- `distribution`: the `dist.py` build pipeline — versioned zips, version baking into
  `bl_info`, git build number, and per-variant file exclusions.

### Modified Capabilities

- None. `openspec/specs/` is empty; every capability is newly introduced.

## Impact

- `openspec/specs/<capability>/spec.md` — 11 new capability specs (after archive).
- `openspec/changes/capture-baseline-specs/` — proposal, design, delta specs, tasks.
- `GLOSSARY.md` — may gain terms surfaced while writing specs; `Undecided` entries must be
  resolved before they are used.
- Source files are read-only references for this change: `hi_five/`, `eevee_next/`,
  `cyclesx/` (`__init__.py`, `properties.py`, `operators.py`, `panel.py`, `scene_builder.py`,
  `crop_canvas.py`), `tests/`, `dist.py`, `hi_five/GUIDE.md`.
- No runtime behavior, API, or dependency changes — `hi_five`, `eevee_next`, and `cyclesx`
  are untouched.

## Non-goals

- Fixing bugs or changing behavior. Quirks are recorded as-is and flagged, not corrected.
- Refactoring code or de-duplicating the three variant copies.
- Adding tests or a variant-drift check; test files are used only as behavioral evidence.
- Specifying internal implementation (function bodies, exact node coordinates, private
  helpers) beyond what behavior requires.
