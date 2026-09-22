## ADDED Requirements

### Requirement: Addon registration
The addon SHALL register its property groups, panels, and operators when enabled, and SHALL expose the toolkit state as `scene.cc_toolkit` and the crop-canvas state as `scene.cc_crop_canvas`.

#### Scenario: Toolkit properties are available after enabling

- **WHEN** the addon is enabled in Blender
- **THEN** every scene exposes `scene.cc_toolkit` and `scene.cc_crop_canvas`

#### Scenario: Panels and operators are registered

- **WHEN** the addon is enabled
- **THEN** the C&C Toolkit sidebar panels and the `ccnc.*` operators can be found in Blender

#### Scenario: Unregistering removes toolkit state

- **WHEN** the addon is disabled
- **THEN** `scene.cc_toolkit` and `scene.cc_crop_canvas` are removed and the registered classes are unregistered

### Requirement: Crop canvas monitor handler
The addon SHALL register the crop-canvas depsgraph monitor on enable and remove it on disable, and SHALL never register the same handler twice.

#### Scenario: Monitor is registered exactly once

- **WHEN** the addon is enabled
- **THEN** the crop-canvas monitor handler appears exactly once in the depsgraph update handlers

#### Scenario: Monitor is removed on disable

- **WHEN** the addon is disabled
- **THEN** the crop-canvas monitor handler is no longer registered

### Requirement: Bundled usage guide
On enable the addon SHALL load its bundled `GUIDE.md` into a Blender text block named "C&C Toolkit Guide".

#### Scenario: Guide text is created

- **WHEN** the addon is enabled and a bundled guide file exists
- **THEN** a text block named "C&C Toolkit Guide" exists containing the guide content

#### Scenario: Missing guide file is tolerated

- **WHEN** the addon is enabled and no bundled guide file exists
- **THEN** enabling completes without error

### Requirement: Version reporting
The addon SHALL report a version string combining the `bl_info` version tuple with a build number, where the build number defaults to `"0"` when no generated build module is present.

#### Scenario: Version string format

- **WHEN** the version is `(0, 3, 0)` and the build number is `42`
- **THEN** the version string reads `0.3.0 (build 42)`

#### Scenario: Build number defaults when absent

- **WHEN** no generated build module is present
- **THEN** the build number is `"0"`
