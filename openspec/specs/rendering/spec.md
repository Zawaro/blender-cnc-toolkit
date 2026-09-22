# rendering Specification

## Purpose
Render Current, Render Animation, the Render + Shadow batch, cancellation, and shadow filter save/restore. Terms: Render Current, Render Animation, Render + Shadow, Frame Offset.
## Requirements
### Requirement: Render Current
Render Current SHALL render the current frame to the output directory using an output filename that adds the frame offset to the current frame number, and SHALL apply the current render type's visibility before rendering.

#### Scenario: Single frame is rendered with offset

- **WHEN** Render Current is triggered with frame offset N on frame F
- **THEN** a PNG is written to the output directory with frame number F + N

#### Scenario: Visibility is applied before rendering

- **WHEN** Render Current is triggered
- **THEN** the current render type's plane visibility is applied before the render

### Requirement: Render Animation
Render Animation SHALL render every frame from the scene start frame to the end frame, applying the current render type's visibility.

#### Scenario: All frames are rendered

- **WHEN** Render Animation is triggered
- **THEN** every frame from start to end is rendered

### Requirement: Render + Shadow batch
When Render Animation runs for the Object or Buildup render type with Render shadow with animation enabled, the toolkit SHALL render the primary pass for all frames and then the Shadow pass for all frames, numbering output frames contiguously. The originally selected render type SHALL be restored when the batch finishes or is cancelled.

#### Scenario: Primary pass then Shadow pass

- **WHEN** Render Animation runs for Object with shadow-with-animation enabled
- **THEN** the Object frames render first, followed by the Shadow frames

#### Scenario: Output numbering is contiguous

- **WHEN** a Render + Shadow batch runs over a frame range of N frames
- **THEN** the Shadow pass frame numbers continue after the primary pass, offset by N

#### Scenario: Shadow pass is skipped when not applicable

- **WHEN** shadow-with-animation is enabled but the render type is not Object or Buildup
- **THEN** only the current render type's frames are rendered

#### Scenario: Render type is restored

- **WHEN** a Render + Shadow batch completes or is cancelled
- **THEN** the originally selected render type is restored

### Requirement: Cancel render
The toolkit SHALL provide a way to stop an ongoing render, clearing the batch and restoring the original render type.

#### Scenario: Stopping a render

- **WHEN** Stop Render is triggered during a batch
- **THEN** the batch is cleared, handlers and timers are removed, and the original render type is restored

### Requirement: Shadow filter save and override
While the render type is Shadow the toolkit SHALL save the current filter size and Cycles filter width, then apply the shadow-only filter overrides. When leaving the Shadow render type the toolkit SHALL restore the saved filter values.

#### Scenario: Shadow saves and overrides the filter

- **WHEN** the render type becomes Shadow
- **THEN** the current filter size and Cycles filter width are saved and the shadow filter overrides are applied

#### Scenario: Leaving Shadow restores the filter

- **WHEN** the render type leaves Shadow
- **THEN** the saved filter size and Cycles filter width are restored
