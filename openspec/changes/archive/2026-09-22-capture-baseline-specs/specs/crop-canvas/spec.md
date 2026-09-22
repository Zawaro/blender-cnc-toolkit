## ADDED Requirements

### Requirement: Crop canvas enable and dimensions
The toolkit SHALL provide a crop canvas toggle and X and Y crop dimensions. When enabled, the render SHALL use a centered crop border sized to those dimensions; when disabled, the full render SHALL be used.

#### Scenario: Crop is enabled

- **WHEN** the crop canvas is enabled with X and Y dimensions
- **THEN** the render uses a centered border of those dimensions

#### Scenario: Crop is disabled

- **WHEN** the crop canvas is disabled
- **THEN** no render border is used and the full render area is used

### Requirement: Crop dimensions are clamped to the render resolution
The crop dimensions SHALL be clamped to the scene render resolution before the border is computed.

#### Scenario: Oversized crop is clamped

- **WHEN** a crop dimension exceeds the render resolution
- **THEN** the effective crop dimension is limited to the render resolution

### Requirement: Crop border is centered
The crop border SHALL be centered on the render, computing equal margins on each side.

#### Scenario: Margins are symmetric

- **WHEN** the crop border is applied
- **THEN** the left and right (and top and bottom) margins around the crop are equal

### Requirement: Crop monitor self-disable
The toolkit SHALL disable the crop canvas when the user clears the render border or crop-to-border outside the toolkit, and SHALL skip this check during modal operations.

#### Scenario: External border removal disables crop

- **WHEN** the crop canvas is enabled and the render border is cleared outside the toolkit
- **THEN** the crop canvas is disabled

#### Scenario: Modal operations are skipped

- **WHEN** a modal operation is active
- **THEN** the crop monitor does not change crop state

### Requirement: Crop canvas panels
The toolkit SHALL present crop controls both in the 3D viewport sidebar and in the output properties format panel, showing the X and Y dimensions only when the crop canvas is enabled.

#### Scenario: Sidebar crop panel

- **WHEN** the C&C Toolkit sidebar is open
- **THEN** the crop canvas panel shows the toggle and the X and Y dimensions

#### Scenario: Output properties crop panel

- **WHEN** the output properties format panel is shown
- **THEN** the crop canvas sub-panel shows the toggle and, when enabled, the X and Y dimensions
