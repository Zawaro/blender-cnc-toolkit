## Context

OpenSpec was initialized with an empty `openspec/specs/`. The addon is a working product: three
near-identical copies (`hi_five` for Blender 5.0+, `eevee_next` for 4.2–4.x, `cyclesx` for
3.0–3.6), a pytest-blender suite covering parts of the behavior, and `dist.py` for packaging.
Behavior is currently defined by the code plus a partial test suite; there is no normative spec.

This change reverse-engineers current behavior into capability specs. It is intentionally
as-built: quirks are recorded, not corrected.

## Goals / Non-Goals

**Goals:**

- Produce a complete, behavior-level capability baseline under `openspec/specs/`.
- Decompose the addon into capabilities with clear seams so future changes target one spec.
- Describe each behavior once, with the three-variant differences isolated in
  `variant-compatibility`.
- Use `GLOSSARY.md` terms verbatim and resolve any `Undecided` term before using it.
- Keep every requirement testable as a WHEN/THEN scenario, using the existing tests as the
  primary evidence where they exist.

**Non-Goals:**

- No code, behavior, or dependency changes; `hi_five`, `eevee_next`, and `cyclesx` are untouched.
- No bug fixes or quirk corrections.
- No code de-duplication across variants.
- No new tests or variant-drift enforcement.
- Not a replacement for `GUIDE.md`; that remains the user-facing guide.

## Decisions

### Decision 1: Capability decomposition over one monolithic spec

Chosen: 11 capability specs keyed by user-observable area (`addon-lifecycle`, `game-config`,
`template-lifecycle`, `scene-construction`, `render-type-visibility`, `compositor`,
`material-remapping`, `rendering`, `crop-canvas`, `variant-compatibility`, `distribution`).

Rationale: OpenSpec archives deltas per capability and matches a capability to a spec folder.
A single spec would make every future change touch one giant file and would blur the contract
between proposal and specs. The seams follow the existing module boundaries closely enough to
be findable, but are behavior-named rather than file-named.

Alternative considered: one spec per source file. Rejected — it mirrors implementation, not
behavior, and would encode the variant triplication.

### Decision 2: Spec once, variant differences centralized

Chosen: each capability describes canonical behavior; `variant-compatibility` holds the
deliberate deviations. The variant-specific extensions (CyclesX denoise, holdout flags, shadow
catcher) live with the compatibility requirements rather than in each capability.

Rationale: the three copies are ~95% identical. Triplicating requirements would create three
sources of truth that drift immediately. Centralizing deltas makes the differences auditable.

Alternative considered: per-variant capabilities. Rejected — ~33 spec folders, near-total
duplication, and no way to see "what is different" in one place.

### Decision 3: Behavior-level requirements, not implementation

Chosen: requirements describe observable outcomes (panel shows X, output is RGBA, frames are
contiguous). Internal details (node coordinates, exact constants, private helpers) are omitted
unless a number is itself behavior (for example the AA/shadow thresholds are recorded because
they change output).

Rationale: a spec that restates implementation rots the moment code changes and provides no
review value. Testable outcomes are the durable contract.

### Decision 4: As-built baseline, with quirks flagged in tasks

Chosen: record current behavior exactly. Where a behavior looks accidental rather than
intended (for example the Debug/Default plane set, engine-dependent matte targets), record it
and note the suspicion in the tasks rather than silently "fixing" the spec.

Rationale: this change must not smuggle in behavior changes. Flagging keeps the option to
open follow-up changes explicit.

### Decision 5: Evidence from tests, code as fallback

Chosen: tests are the first source for scenarios where they exist (`test_config`,
`test_visibility`, `test_render`, `test_scene_state`, `test_rebuild`, `test_compositor`,
`test_registration`, `test_properties`). `crop-canvas`, `variant-compatibility`, and
`distribution` have no tests and are spec'd from code directly, so their scenarios are
assertions not yet covered by any check.

## Risks / Trade-offs

- **Spec as a second copy of code** → Requirements stay behavior-level and scenario-based; no
  function names or node wiring in normative text.
- **Compositor spec is large and detail-heavy** → It is grouped by render type so each
  requirement maps to one visible output; future changes modify one render-type requirement.
- **Baseline may record a bug as intended** → Decision 4 flags suspects in tasks; a follow-up
  change can correct the spec deliberately.
- **Untested capabilities may be spec'd inaccurately** → Those capabilities are marked in
  tasks as "code as evidence" so a reviewer knows where to look hardest.
- **Archive seeds `## Purpose` as "TBD"** → Tasks include filling in each archived spec's
  Purpose immediately after archiving.

## Migration Plan

1. Write the 11 delta specs (this change), proposal, design, and tasks.
2. Validate the change.
3. Archive the change, producing `openspec/specs/<capability>/spec.md` for each capability.
4. Fill in the "TBD" Purpose section of each archived spec.
5. Confirm no source file under `hi_five/`, `eevee_next/`, or `cyclesx/` was modified.

Rollback: the change lives only under `openspec/`; reverting the branch restores the empty
spec set with no impact on the addon.

## Open Questions

- Should the two `Undecided`-worthy terms surfaced here (for example the "Default" render type
  behavior versus its name) become glossary entries? Resolve before any spec wording depends
  on them.
- Should `crop-canvas`, `variant-compatibility`, and `distribution` eventually gain tests so
  their scenarios become verified rather than aspirational? Out of scope here; candidate
  follow-up.

## Known quirks (recorded as-is)

These behaviors are captured exactly as the code and `RENDER_TYPE_VIS` define them. Each is a
candidate follow-up, not a correction:

- **3.1 Render-type visibility vs names and guide.** `RENDER_TYPE_VIS` shows: Default — grey
  only; Preview — holdout + shadow (ambient hidden); Object — ambient only (grey hidden);
  Buildup — holdout2 only (shadow2 hidden); Shadow — holdout only. `GUIDE.md` describes Preview
  as including ambient occlusion and Buildup as using a secondary shadow catcher, which does
  not match the ambient/holdout2 entries. The table and `tests/test_visibility.py` agree with
  each other; the guide wording is the outlier.
- **3.2 Shadow matte target differs by engine — intentional.** The Shadow render type reads the
  shadow plane's Cryptomatte under Cycles but the holdout plane's Cryptomatte under Eevee
  (`create_compositor` / `_wire_shadow`). This is deliberate: Eevee has no native shadow
  catcher, so Eevee needs a workaround and Cycles and Eevee are otherwise unrelated engines.
  Recorded as intended behavior, not a candidate bug.
- **3.3 Cycles-only sun hiding and CyclesX Cycles-only shadow catcher.** The toolkit sun is
  hidden from render whenever the engine is Cycles (`apply_render_type_visibility`), and in
  CyclesX the shadow planes are shadow catchers only when the engine is Cycles
  (`create_planes`). Recorded, not judged.
