# game-config Specification

## Purpose
Game, Variant, Engine, and Camera mode selection, plus game-configuration resolution, engine mapping, and the render-type visibility table. Terms: Game, Game config, Variant, Engine, Camera mode, Render type.
## Requirements
### Requirement: Game selection
The toolkit SHALL offer six game targets: Red Alert 2 (`RA2`), Tiberian Sun (`TS`), ReWire (`RW`), Red Alert / Tiberian Dawn (`RA1`), C&C Remastered (`RM`), and Dune 2000 (`D2K`). Red Alert 2 SHALL be the default.

#### Scenario: All games are offered

- **WHEN** the game selector is shown
- **THEN** exactly the six game targets above are available with no duplicates

#### Scenario: Default game

- **WHEN** a fresh scene is used
- **THEN** the selected game is Red Alert 2

### Requirement: Variant selection
The toolkit SHALL offer three variants: Base (`BASE`), Infantry (`INF`), and Effects (`FX`). Base SHALL be the default.

#### Scenario: All variants are offered

- **WHEN** the variant selector is shown
- **THEN** exactly Base, Infantry, and Effects are available with no duplicates

### Requirement: Engine selection
The toolkit SHALL offer two engines: Cycles (`CYCLES`) and Eevee (`EEVEE`). Cycles SHALL be the default.

#### Scenario: All engines are offered

- **WHEN** the engine selector is shown
- **THEN** Cycles and Eevee are available with no duplicates

### Requirement: Camera mode availability
The toolkit SHALL offer a camera mode of Perspective (`PERSP`) or Isometric (`ORTHO`) only for Red Alert / Tiberian Dawn, C&C Remastered, and Dune 2000. For the other games the camera mode SHALL NOT be shown. Isometric SHALL be the default.

#### Scenario: Camera mode shown for supporting games

- **WHEN** the selected game is RA1, RM, or D2K
- **THEN** the camera-mode selector is shown

#### Scenario: Camera mode hidden for other games

- **WHEN** the selected game is RA2, TS, or RW
- **THEN** the camera-mode selector is not shown

### Requirement: Configuration resolution
The toolkit SHALL resolve a game configuration for any game and variant combination. A variant without an explicit override SHALL inherit the game's base configuration. An unknown game SHALL resolve to the Red Alert 2 base configuration, and an unknown variant SHALL resolve to the selected game's base configuration.

#### Scenario: Known game and variant

- **WHEN** a configuration is requested for a known game and variant with overrides
- **THEN** the returned configuration contains those override values

#### Scenario: Variant inherits base

- **WHEN** a variant has no explicit override for a value
- **THEN** the returned configuration carries the base value for that field

#### Scenario: Unknown game falls back

- **WHEN** a configuration is requested for an unknown game
- **THEN** the Red Alert 2 base configuration is returned

#### Scenario: Unknown variant falls back

- **WHEN** a configuration is requested for a known game and an unknown variant
- **THEN** that game's base configuration is returned

### Requirement: Engine mapping
The toolkit SHALL map its engine choices to Blender render engines: Cycles maps to the Cycles engine, and Eevee maps to the variant's Eevee engine identifier.

#### Scenario: Cycles maps to Cycles

- **WHEN** the engine is `CYCLES`
- **THEN** the resolved Blender render engine is Cycles

#### Scenario: Eevee maps to the variant Eevee engine

- **WHEN** the engine is `EEVEE`
- **THEN** the resolved Blender render engine is the Eevee engine identifier for that addon variant

### Requirement: Render type visibility table
The toolkit SHALL define plane visibility for each of the five render types (Default, Preview, Object, Buildup, Shadow) across the seven planes (holdout, holdout2, shadow, shadow2, blue, grey, ambient), where each plane value is either visible or hidden.

#### Scenario: All render types are defined

- **WHEN** the visibility table is inspected
- **THEN** it contains exactly Default, Preview, Object, Buildup, and Shadow

#### Scenario: Every render type covers every plane

- **WHEN** any render type's visibility is inspected
- **THEN** it defines a value for each of the seven planes

#### Scenario: Visibility values are binary

- **WHEN** any plane value in the table is inspected
- **THEN** it is either visible or hidden
