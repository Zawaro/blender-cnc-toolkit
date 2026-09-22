# scene-construction Specification

## Purpose
Building the toolkit collections, camera, sun, world, Render planes, and Boolean cutter. Terms: Render plane, Boolean cutter, `_CNC_Toolkit` collection.
## Requirements
### Requirement: Toolkit collections
A rebuild SHALL create a root `_CNC_Toolkit` collection linked to the scene, containing child collections for shadow planes and holdout planes.

#### Scenario: Collections are created

- **WHEN** the template is rebuilt
- **THEN** the `_CNC_Toolkit` collection exists with `_CNC_Toolkit Shadow` and `_CNC_Toolkit Holdout` children

### Requirement: Camera creation
The toolkit SHALL create a camera from the resolved game configuration and camera mode, make it the scene camera, and switch an open 3D viewport to camera view. For games supporting Isometric mode, Isometric SHALL use the isometric camera transforms; otherwise the configuration's camera transforms SHALL be used.

#### Scenario: Camera is created and set

- **WHEN** the template is rebuilt
- **THEN** a toolkit camera exists, is the scene camera, and an open 3D viewport is in camera view

#### Scenario: Isometric camera uses isometric transforms

- **WHEN** a game supporting camera mode is rebuilt in Isometric mode
- **THEN** the camera uses the isometric location, rotation, and ortho scale

#### Scenario: Perspective camera

- **WHEN** a game is rebuilt in Perspective mode
- **THEN** the camera is a perspective camera using the configuration's lens settings

### Requirement: Sun light creation
The toolkit SHALL create a sun light from the resolved configuration, positioned and rotated per configuration, non-selectable, and hidden from render.

#### Scenario: Sun is created

- **WHEN** the template is rebuilt
- **THEN** a toolkit sun exists with the configured energy, angle, location, and rotation, and is hidden from render

### Requirement: World creation
The toolkit SHALL create a toolkit world from the resolved configuration, set it as the scene world, and build its node tree to provide the game's sky and environment for the active engine.

#### Scenario: World is created and assigned

- **WHEN** the template is rebuilt
- **THEN** a toolkit world exists, is the scene world, and provides sky/environment shading for the active engine

### Requirement: Render planes
The toolkit SHALL create seven planes — ambient, blue, grey, holdout, holdout2, shadow, and shadow2 — each with the matching toolkit material, hidden from render and viewport by default. The holdout plane SHALL be placed slightly below the other planes, and shadow planes SHALL be shadow catchers.

#### Scenario: All planes are created

- **WHEN** the template is rebuilt
- **THEN** all seven toolkit planes exist with their matching materials

#### Scenario: Planes start hidden

- **WHEN** the template is rebuilt
- **THEN** every plane is hidden from render and viewport until render-type visibility is applied

#### Scenario: Shadow planes catch shadows

- **WHEN** the template is rebuilt
- **THEN** both shadow planes are configured as shadow catchers

### Requirement: Boolean cutter
When a boolean cutter object is selected, the toolkit SHALL apply a difference boolean modifier using that cutter to every render plane, hide the cutter from render, and display it as a wireframe. Removing the cutter SHALL remove the modifiers and restore the cutter's original display type.

#### Scenario: Cutter applies to all planes

- **WHEN** a boolean cutter is selected while a template is generated
- **THEN** every render plane has a difference boolean modifier referencing the cutter

#### Scenario: Cutter is hidden and shown as wireframe

- **WHEN** a boolean cutter is selected
- **THEN** the cutter is hidden from render and displayed as a wireframe

#### Scenario: Removing the cutter restores display

- **WHEN** the boolean cutter is cleared
- **THEN** the boolean modifiers are removed and the cutter's original display type is restored
