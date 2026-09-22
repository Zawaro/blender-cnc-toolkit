## ADDED Requirements

### Requirement: Plane visibility per render type
The toolkit SHALL set each render plane's render visibility from the selected render type's visibility table, where a table value of `1` hides the plane from render and `0` shows it. The visible planes SHALL be: Default — grey only; Preview — holdout and shadow; Object — ambient only; Buildup — holdout2 only; Shadow — holdout only.

#### Scenario: Default shows only the grey plane

- **WHEN** the render type is Default
- **THEN** only the grey plane is visible to render and every other plane is hidden

#### Scenario: Preview shows the holdout and shadow planes

- **WHEN** the render type is Preview
- **THEN** the holdout and shadow planes are visible to render and every other plane is hidden

#### Scenario: Object shows only the ambient plane

- **WHEN** the render type is Object
- **THEN** the ambient plane is visible to render and every other plane is hidden

#### Scenario: Buildup shows only the secondary holdout plane

- **WHEN** the render type is Buildup
- **THEN** the holdout2 plane is visible to render and every other plane is hidden

#### Scenario: Shadow shows only the holdout plane

- **WHEN** the render type is Shadow
- **THEN** the holdout plane is visible to render and every other plane is hidden

### Requirement: Holdout collection exclusion
The toolkit SHALL exclude or include the `_CNC_Toolkit Holdout` collection from the view layer so that the holdout plane is present only for render types whose visibility table marks the holdout plane visible.

#### Scenario: Holdout collection is excluded when hidden

- **WHEN** the render type marks the holdout plane hidden
- **THEN** the `_CNC_Toolkit Holdout` collection is excluded from the view layer

#### Scenario: Holdout collection is included when visible

- **WHEN** the render type marks the holdout plane visible
- **THEN** the `_CNC_Toolkit Holdout` collection is included in the view layer

### Requirement: Sun visibility by engine
The toolkit SHALL hide the toolkit sun from render when the engine is Cycles and SHALL show it otherwise.

#### Scenario: Cycles hides the sun

- **WHEN** the engine is Cycles
- **THEN** the toolkit sun is hidden from render

#### Scenario: Eevee shows the sun

- **WHEN** the engine is Eevee
- **THEN** the toolkit sun is not hidden from render

### Requirement: Unknown render type fallback
When the selected render type is not present in the visibility table, the toolkit SHALL apply the Object render type's visibility.

#### Scenario: Unknown render type uses Object visibility

- **WHEN** an unknown render type is applied
- **THEN** the Object render type's plane, collection, and sun visibility is used
