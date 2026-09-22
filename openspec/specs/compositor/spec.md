# compositor Specification

## Purpose
The compositor built per Render type: Alpha Convert, background and transparency handling, shadow tint, and output color mode. Terms: Compositor tree, Alpha Convert, Transparent background, Anti-aliasing against background, Shadow catcher.
## Requirements
### Requirement: Compositor creation
The toolkit SHALL create a toolkit compositor for the selected render type and attach it to the scene, replacing any previous toolkit compositor. Every compositor build SHALL provide a reusable Alpha Convert node group.

#### Scenario: Compositor is attached

- **WHEN** the compositor is rebuilt
- **THEN** a toolkit compositor is attached to the scene

#### Scenario: Previous toolkit compositor is replaced

- **WHEN** the compositor is rebuilt while a previous toolkit compositor exists
- **THEN** the previous toolkit compositor and its toolkit node groups are removed before the new one is built

#### Scenario: Alpha Convert node group is available

- **WHEN** the compositor is rebuilt
- **THEN** an Alpha Convert node group exists and is available to the compositor

### Requirement: Default render type compositor
For the Default render type the toolkit SHALL output the render layer directly, SHALL disable film transparency, and SHALL output RGB.

#### Scenario: Default outputs RGB without transparency

- **WHEN** the render type is Default and the compositor is rebuilt
- **THEN** film transparency is off and the output color mode is RGB

### Requirement: Preview render type compositor
For the Preview render type the toolkit SHALL composite a shadow tint over the background, using the shadow plane's Cryptomatte and the shadow color and opacity, and SHALL support a background image in place of the background color.

#### Scenario: Preview composites a shadow tint

- **WHEN** the render type is Preview and the compositor is rebuilt
- **THEN** the output composites the shadow tint over the background

#### Scenario: Preview shadow opacity applies

- **WHEN** the shadow opacity is set in Preview
- **THEN** the shadow tint's strength reflects that opacity

#### Scenario: Preview uses a background image when enabled

- **WHEN** a background image is enabled with a valid path in Preview
- **THEN** the background image is used in place of the background color

#### Scenario: Preview keeps the background color when the image is unavailable

- **WHEN** a background image is enabled but the path is missing
- **THEN** the background color is used

### Requirement: Object and Buildup render type compositor
For the Object and Buildup render types the toolkit SHALL composite the render over the background color, hiding the background where the object's alpha excludes it.

#### Scenario: Object composites over background

- **WHEN** the render type is Object and the compositor is rebuilt
- **THEN** the output composites the render over the background color

#### Scenario: Buildup composites over background

- **WHEN** the render type is Buildup and the compositor is rebuilt
- **THEN** the output composites the render over the background color

### Requirement: Transparent background output
When transparent background is enabled for the Object, Buildup, or Preview render types, the toolkit SHALL output RGBA. When transparent background is disabled, the toolkit SHALL output RGB with a solid background.

#### Scenario: Transparent background outputs RGBA

- **WHEN** transparent background is enabled for a supported render type
- **THEN** the output color mode is RGBA and PNG output is used

#### Scenario: Opaque background outputs RGB

- **WHEN** transparent background is disabled for a supported render type
- **THEN** the output color mode is RGB with a solid background color

### Requirement: Anti-aliasing against background
When anti-aliasing against background is enabled together with transparent background, the toolkit SHALL bypass the Alpha Convert node group and use native film transparency for smooth object edges.

#### Scenario: AA against background bypasses Alpha Convert

- **WHEN** anti-aliasing against background and transparent background are both enabled
- **THEN** the compositor bypasses the Alpha Convert node group and uses film transparency

### Requirement: Shadow render type compositor
For the Shadow render type the toolkit SHALL produce a shadow-only output tinted with the shadow color, using the shadow plane's Cryptomatte under Cycles and the holdout plane's Cryptomatte under Eevee, and SHALL output RGBA with film transparency.

#### Scenario: Shadow outputs a tinted shadow

- **WHEN** the render type is Shadow and the compositor is rebuilt
- **THEN** the output is a shadow tinted with the shadow color over the background

#### Scenario: Shadow matte target depends on engine

- **WHEN** the render type is Shadow under Cycles
- **THEN** the shadow plane is used as the matte source
- **WHEN** the render type is Shadow under Eevee
- **THEN** the holdout plane is used as the matte source

#### Scenario: Shadow outputs RGBA

- **WHEN** the render type is Shadow
- **THEN** the output color mode is RGBA with film transparency

### Requirement: Node arrangement
After every rebuild the toolkit SHALL arrange its compositor node trees.

#### Scenario: Nodes are arranged on rebuild

- **WHEN** the compositor is rebuilt
- **THEN** the toolkit node trees are laid out
