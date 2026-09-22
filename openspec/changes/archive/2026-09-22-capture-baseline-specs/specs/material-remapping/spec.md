## ADDED Requirements

### Requirement: Remap material picker excludes toolkit materials
The remap material picker SHALL exclude any material whose name starts with the toolkit prefix.

#### Scenario: Toolkit materials are not selectable

- **WHEN** the remap material picker is shown
- **THEN** toolkit-prefixed materials cannot be selected

### Requirement: Add remap material
Adding a remap material SHALL reject toolkit materials and materials already in the list, SHALL discard blank entries, and SHALL add the selected material to the remap list. When a template is generated, adding a material SHALL rebuild the compositor.

#### Scenario: Material is added

- **WHEN** a non-toolkit material is added and is not already in the list
- **THEN** it is added to the remap list and the picker is cleared

#### Scenario: Toolkit material is rejected

- **WHEN** a toolkit-prefixed material is added
- **THEN** the addition is cancelled with a warning

#### Scenario: Duplicate material is rejected

- **WHEN** a material already in the remap list is added again
- **THEN** the addition is cancelled with a warning

#### Scenario: Blank entries are discarded

- **WHEN** a remap material is added while the list contains blank entries
- **THEN** the blank entries are removed

#### Scenario: Adding rebuilds the compositor

- **WHEN** a material is added while a template is generated
- **THEN** the compositor is rebuilt

### Requirement: Remove and clear remap materials
The toolkit SHALL remove a selected remap material by index and SHALL clear the entire remap list. When a template is generated, removing or clearing SHALL rebuild the compositor.

#### Scenario: A material is removed

- **WHEN** a remap material is removed by index
- **THEN** that entry is removed from the list

#### Scenario: The list is cleared

- **WHEN** Clear All is used
- **THEN** the remap list is empty

#### Scenario: Removal rebuilds the compositor

- **WHEN** a material is removed or the list is cleared while a template is generated
- **THEN** the compositor is rebuilt

### Requirement: Remap color and Cryptomatte pass
The toolkit SHALL apply the selected remap color to the remapped materials in the compositor and SHALL enable the Cryptomatte material pass, including its depth, while remap materials are present.

#### Scenario: Cryptomatte material pass is enabled

- **WHEN** the rebuild runs while remap materials are present
- **THEN** the Cryptomatte material pass is enabled

#### Scenario: Cryptomatte material pass is disabled when unused

- **WHEN** the rebuild runs with no remap materials
- **THEN** the Cryptomatte material pass is disabled

#### Scenario: Remap color is applied

- **WHEN** the compositor is built with remap materials and a remap color
- **THEN** the remapped materials are tinted toward the remap color
