# Glossary

Canonical term directory for Blender C&C Toolkit. Fast lookup — the full meaning
lives in the code (authoritative) or the anchored spec. Grouped by domain cluster.

**Rule:** read this before writing specs/design docs or naming things. When a term
surfaces during planning or clarifying — even a prompt-only term — propose adding it
here. See **Undecided** below for terms that must not be guessed.

Entry form: term → one-line meaning → anchor. Line anchors reference `hi_five/`
(the primary variant); the same symbols exist in `eevee_next/` and `cyclesx/`.

## Scene & Build

| Term | Meaning | Where |
|------|---------|-------|
| Template scene | Blender scene pre-configured for rendering C&C sprites: camera, sun, world HDRI, shadow/holdout planes, compositor tree. Applied by the addon, fully mutable. | `rebuild_all` hi_five/scene_builder.py:227 |
| Full mutation | On game/variant/engine change, template elements are deleted and rebuilt from scratch. User objects outside `_CNC_Toolkit` are preserved. | `rebuild_all` hi_five/scene_builder.py:227 |
| `_CNC_Toolkit` collection | Collection owning every generated template object, split into sub-collections (e.g. `_CNC_Toolkit Holdout`). The boundary between generated and user content. | `COLLECTION_NAME` hi_five/scene_builder.py:14 |
| `_CNC_` prefix | Naming prefix on every generated object, material, world, and compositor tree. Used to detect and clean up addon content. | `PREFIX` hi_five/scene_builder.py:13 |
| Render plane | One of the seven generated planes (ambient, blue, grey, holdout, holdout2, shadow, shadow2) that supply the background, shadow, and holdout surfaces. Visibility is per render type. | `create_planes` hi_five/scene_builder.py:614 |
| Boolean cutter | User mesh object used as a difference cutter applied to every render plane during a rebuild. | `apply_boolean_modifier` hi_five/scene_builder.py:266 |

## Variants & Rendering

| Term | Meaning | Where |
|------|---------|-------|
| Game | C&C title target: `RA2`, `TS`, `RW`, `RA1`, `RM`, `D2K`. Drives resolution, camera, sun, sky, HDRI. | `GAME_ITEMS` hi_five/properties.py:3 · `GAME_CONFIGS` hi_five/scene_builder.py:59 |
| Game config | Per-game × per-variant parameter set (resolution, camera, sun, sky, HDRI), resolved by `get_config`. Unknown game/variant falls back to `RA2` / `BASE`. | `get_config` hi_five/scene_builder.py:99 |
| Variant | Sprite subtype that changes resolution, camera ortho scale, and lighting: `BASE` (Base), `INF` (Infantry), `FX` (Effects). | `VARIANT_ITEMS` hi_five/properties.py:12 |
| Engine | Render engine: `CYCLES` or `EEVEE`. Mapped to Blender's engine id via `ENGINE_MAP`. | `ENGINE_ITEMS` hi_five/properties.py:18 · `ENGINE_MAP` hi_five/scene_builder.py:17 |
| Camera mode | `PERSP` (original 3D perspective) or `ORTHO` (standard C&C isometric). | `CAMERA_MODE_ITEMS` hi_five/properties.py:23 |
| Render type | Which planes are visible and how the compositor is wired: `DEFAULT`, `PREVIEW`, `OBJECT`, `BUILDUP`, `SHADOW`. | `RENDER_TYPE_ITEMS` hi_five/properties.py:29 · `apply_render_type_visibility` hi_five/scene_builder.py:1084 |
| Default render type | Shows only the grey reference plane against the scene background, no compositor processing. Baseline state. | `RENDER_TYPE_VIS["DEFAULT"]` hi_five/scene_builder.py:1075 |
| Shadow plane / Holdout plane | Generated planes: shadow planes catch shadows, holdout planes mask the object's silhouette. Visibility is per render type. | `RENDER_TYPE_VIS` hi_five/scene_builder.py:1075 |
| Shadow catcher | Surface that captures only shadows. Cycles supports it natively; Eevee does not, so Eevee uses a holdout-plane workaround for the Shadow render type. | `_wire_shadow` hi_five/scene_builder.py:920 |
| Compositor tree | Node tree (`_CNC_Composition`) built per render type; includes the `_CNC_Alpha Convert` node group. | `create_compositor` hi_five/scene_builder.py:645 |

## Output & Compositing

| Term | Meaning | Where |
|------|---------|-------|
| Render + Shadow | Batch operator that renders the primary pass (Object or Buildup) then the Shadow pass with an auto-calculated frame offset so output filenames are contiguous. | `render_shadow_with_animation` hi_five/properties.py:153 |
| Frame Offset | User number added to output frame filenames for single-pass renders. Auto-calculated for Render + Shadow. | `frame_offset` hi_five/properties.py:145 |
| Anti-aliasing against background | When on, the compositor bypasses the Alpha Convert node group and uses native `film_transparent` alpha for smooth object edges. | `aa_against_bg` hi_five/properties.py:159 |
| Transparent background | When on, outputs RGBA and blocks background colors/planes; when off, outputs RGB with a solid background and all visible planes pass through. | `transparent_bg` hi_five/properties.py:166 · `create_compositor` hi_five/scene_builder.py:645 |
| Alpha Convert | Node group (`_CNC_Alpha Convert`) that derives alpha from HSV brightness so the rendered planes composite cleanly. | `ALPHA_CONVERT_NAME` hi_five/scene_builder.py:16 · `create_compositor` hi_five/scene_builder.py:645 |
| Cryptomatte | Matte source used by the compositor to isolate a plane or material (e.g. the shadow plane, or remapped materials). | `_create_remap_hue` hi_five/scene_builder.py:714 |
| Remap material | User material whose hue is shifted toward the remap color in the compositor, to make color variants of a sprite. | `CNC_OT_add_remap_material` hi_five/operators.py:162 |
| Crop canvas | Cropped render border that limits output to centered X/Y dimensions independent of the game resolution. | `CropCanvasProperties` hi_five/crop_canvas.py:4 |

## Addon & Build

| Term | Meaning | Where |
|------|---------|-------|
| Render Current | Renders only the current frame to the output directory, applying the frame offset to the filename. | `CNC_OT_render` hi_five/operators.py:38 |
| Render Animation | Renders every frame from the scene start to end; optionally runs a Shadow pass after the primary pass. | `CNC_OT_render_shadow` hi_five/operators.py:56 |
| Distribution build | `dist.py` packaging of a variant into a versioned zip with the version baked into `bl_info` and a git build number. | `zip_addon` dist.py:48 |

## Adding terms

1. Propose the term with a one-line meaning and the code/spec anchor.
2. Get developer approval.
3. Add a row to the matching cluster (or a new one).
4. Use the term verbatim in code, specs, and docs.

## Undecided

Terms that must not be guessed — propose an entry before using them:

- *(none yet)*
