# template-lifecycle Specification

## Purpose
Generating and purging the Template scene, full mutation on parameter change, and pre-template scene-state save/restore. Terms: Template scene, Full mutation, `_CNC_Toolkit` collection.
## Requirements
### Requirement: Generate Template
On first generation the toolkit SHALL snapshot the pre-template scene state, apply the initial settings for the selected game, variant, and engine, rebuild the template scene, and mark the template as generated. On subsequent generations of the same scene it SHALL NOT overwrite the saved snapshot.

#### Scenario: First generation snapshots and builds

- **WHEN** Generate Template is triggered on a scene without a generated template
- **THEN** the pre-template state is saved, initial settings are applied, the template is rebuilt, and the template is marked generated

#### Scenario: Regeneration keeps the original snapshot

- **WHEN** Generate Template is triggered while a template is already generated
- **THEN** the existing saved snapshot is not overwritten and the template is rebuilt

### Requirement: Full mutation on parameter change
The toolkit SHALL rebuild the template scene when the game, variant, or camera mode changes while a template is generated, and SHALL rebuild only the compositor when the engine, render type, or compositor-affecting setting changes.

#### Scenario: Rebuild the whole template on game change

- **WHEN** the game, variant, or camera mode changes while a template is generated
- **THEN** the template elements are deleted and rebuilt from scratch

#### Scenario: Rebuild only the compositor on engine change

- **WHEN** the engine changes while a template is generated
- **THEN** the compositor is rebuilt without destroying the template elements

#### Scenario: Rebuild on background and shadow settings

- **WHEN** a compositor-affecting setting such as render type, background color, transparent background, anti-aliasing, shadow color, shadow opacity, background image, or remap color changes
- **THEN** the compositor is rebuilt

### Requirement: Purge Template
Purge Template SHALL remove all generated template data, restore the saved pre-template scene state, and clear the generated flag and saved snapshot.

#### Scenario: Purge restores the scene

- **WHEN** Purge Template is triggered
- **THEN** all `_CNC_` template data is removed, the saved state is restored, and the template is no longer marked generated

### Requirement: Scene state snapshot and restore
The toolkit SHALL snapshot and restore the resolution, render engine, frame rate, film transparency, color mode, file format, world, compositor, filter size, and Cycles filter width. Restoring SHALL tolerate a saved world or compositor that no longer exists.

#### Scenario: Snapshot captures render and world state

- **WHEN** a scene state is saved
- **THEN** the snapshot contains the resolution, engine, frame rate, film transparency, color mode, file format, world, compositor, filter size, and Cycles filter width

#### Scenario: Restore round-trips values

- **WHEN** a scene state is saved and later restored
- **THEN** the saved render and world values are applied back to the scene

#### Scenario: Deleted world or compositor is tolerated

- **WHEN** a snapshot is restored but the saved world or compositor no longer exists
- **THEN** restoring completes without error

#### Scenario: Empty or invalid snapshot is tolerated

- **WHEN** restore is attempted with no snapshot or an invalid snapshot
- **THEN** restoring completes without error

### Requirement: Toolkit data cleanup
Clearing the template SHALL remove all collections whose names contain the toolkit prefix, all toolkit-prefixed materials, worlds, node groups, and images, all toolkit-prefixed objects, and SHALL detach a toolkit-prefixed scene compositor.

#### Scenario: Toolkit collections and data are removed

- **WHEN** the template is cleared
- **THEN** no toolkit-prefixed collections, materials, worlds, node groups, images, or objects remain

#### Scenario: Toolkit compositor is detached

- **WHEN** the template is cleared while the scene uses a toolkit compositor
- **THEN** the scene compositor is detached

### Requirement: User content preservation
Clearing and rebuilding SHALL preserve objects outside the `_CNC_Toolkit` collection.

#### Scenario: Imported objects survive a rebuild

- **WHEN** the template is rebuilt while the scene contains objects outside the toolkit collection
- **THEN** those objects remain in the scene

### Requirement: Active collection restoration
After a rebuild the toolkit SHALL restore the previously active collection, falling back to the scene root when the previously active collection was a toolkit collection.

#### Scenario: User collection is restored

- **WHEN** the template is rebuilt while a user collection was active
- **THEN** that user collection is active again after the rebuild

#### Scenario: Toolkit collection falls back to root

- **WHEN** the template is rebuilt while a toolkit collection was active
- **THEN** the scene root collection is active after the rebuild

### Requirement: Crop canvas refresh after rebuild
The toolkit SHALL refresh the crop canvas resolution at the end of every rebuild when the crop canvas is enabled, so displayed dimensions are not stale.

#### Scenario: Crop refresh on rebuild

- **WHEN** the template is rebuilt with the crop canvas enabled
- **THEN** the crop canvas resolution is refreshed from the rebuilt scene
