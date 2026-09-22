## ADDED Requirements

### Requirement: Variant engine mapping
Each addon variant SHALL map the Eevee engine choice to the Eevee render engine identifier supported by its Blender version. HiFive SHALL map Eevee to `BLENDER_EEVEE`; Eevee Next SHALL map Eevee to `BLENDER_EEVEE_NEXT`; CyclesX SHALL map Eevee to `BLENDER_EEVEE`. All variants SHALL map Cycles to `CYCLES`.

#### Scenario: HiFive engine mapping

- **WHEN** HiFive resolves the engine `EEVEE`
- **THEN** the Blender engine is `BLENDER_EEVEE`

#### Scenario: Eevee Next engine mapping

- **WHEN** Eevee Next resolves the engine `EEVEE`
- **THEN** the Blender engine is `BLENDER_EEVEE_NEXT`

#### Scenario: CyclesX engine mapping

- **WHEN** CyclesX resolves the engine `EEVEE`
- **THEN** the Blender engine is `BLENDER_EEVEE`

### Requirement: Variant compositor node APIs
The addon variants SHALL use the color-separation node APIs available in their Blender version. HiFive SHALL use `CompositorNodeSeparateColor` / `CompositorNodeCombineColor`; Eevee Next and CyclesX SHALL use `CompositorNodeSepHSVA` / `CompositorNodeCombHSVA`.

#### Scenario: HiFive uses Blender 5 color nodes

- **WHEN** HiFive builds the Alpha Convert group or a shadow separation
- **THEN** it uses `CompositorNodeSeparateColor` and `CompositorNodeCombineColor`

#### Scenario: Eevee Next uses legacy HSV nodes

- **WHEN** Eevee Next builds the Alpha Convert group or a shadow separation
- **THEN** it uses `CompositorNodeSepHSVA` and `CompositorNodeCombHSVA`

#### Scenario: CyclesX uses legacy HSV nodes

- **WHEN** CyclesX builds the Alpha Convert group or a shadow separation
- **THEN** it uses `CompositorNodeSepHSVA` and `CompositorNodeCombHSVA`

### Requirement: Variant compositor container
HiFive SHALL attach its compositor through the scene compositing node group. Eevee Next and CyclesX SHALL attach their compositor through the scene's default compositor node tree, enabling scene nodes and clearing existing nodes first.

#### Scenario: HiFive uses the compositing node group

- **WHEN** HiFive attaches its compositor
- **THEN** the scene compositing node group is set to the toolkit compositor

#### Scenario: Eevee Next uses the scene node tree

- **WHEN** Eevee Next attaches its compositor
- **THEN** scene nodes are enabled and the toolkit compositor is built in the scene node tree

#### Scenario: CyclesX uses the scene node tree

- **WHEN** CyclesX attaches its compositor
- **THEN** scene nodes are enabled and the toolkit compositor is built in the scene node tree

### Requirement: Variant world node setup
Eevee Next and CyclesX SHALL explicitly enable world node trees before building the toolkit world. HiFive SHALL build the world node tree without an explicit enable step.

#### Scenario: Eevee Next enables world nodes

- **WHEN** Eevee Next builds the toolkit world
- **THEN** world node usage is explicitly enabled

#### Scenario: CyclesX enables world nodes

- **WHEN** CyclesX builds the toolkit world
- **THEN** world node usage is explicitly enabled

### Requirement: Variant sky configuration
HiFive SHALL configure the world sky with single scattering. Eevee Next SHALL configure the world sky with the Nishita sky type and a dust density. CyclesX SHALL configure the world sky with the Nishita sky type and a dust density under its sky path.

#### Scenario: HiFive sky type

- **WHEN** HiFive builds the toolkit world
- **THEN** the sky uses single scattering

#### Scenario: Eevee Next sky type

- **WHEN** Eevee Next builds the toolkit world
- **THEN** the sky uses the Nishita type with a dust density

#### Scenario: CyclesX sky type

- **WHEN** CyclesX builds the toolkit world through its sky path
- **THEN** the sky uses the Nishita type with a dust density

### Requirement: Variant holdout behavior
CyclesX SHALL implement holdout planes using a holdout object flag in addition to the holdout material and collection. HiFive and Eevee Next SHALL implement holdout planes using the holdout material and collection without a holdout object flag.

#### Scenario: CyclesX marks holdout objects

- **WHEN** CyclesX creates holdout planes
- **THEN** those planes are configured as holdout objects

#### Scenario: HiFive does not use holdout objects

- **WHEN** HiFive creates holdout planes
- **THEN** no holdout object flag is set

### Requirement: Variant shadow catcher
CyclesX SHALL configure shadow planes as shadow catchers only when the engine is Cycles. HiFive and Eevee Next SHALL configure shadow planes as shadow catchers.

#### Scenario: CyclesX shadow catcher depends on engine

- **WHEN** CyclesX rebuilds with the Cycles engine
- **THEN** the shadow planes are shadow catchers

#### Scenario: CyclesX Eevee shadow planes

- **WHEN** CyclesX rebuilds with the Eevee engine
- **THEN** the shadow planes are not shadow catchers

### Requirement: CyclesX denoise capability
CyclesX SHALL provide a denoise capability with separate composite and render denoise toggles that drive Cycles and compositor denoising. HiFive and Eevee Next SHALL NOT provide these toggles.

#### Scenario: CyclesX exposes denoise toggles

- **WHEN** CyclesX is enabled
- **THEN** the denoise panel offers the composite and render denoise toggles

#### Scenario: CyclesX render denoise configures Cycles

- **WHEN** CyclesX render denoise is enabled
- **THEN** Cycles denoising is enabled for rendering

#### Scenario: CyclesX composite denoise configures the compositor

- **WHEN** CyclesX composite denoise is enabled
- **THEN** a denoise node is inserted into the compositor

#### Scenario: Other variants have no denoise toggles

- **WHEN** HiFive or Eevee Next is enabled
- **THEN** no denoise toggle is offered

### Requirement: Variant distribution packaging
The distribution build SHALL exclude the Blender manifest from the CyclesX package while including it for HiFive and Eevee Next.

#### Scenario: CyclesX package omits the manifest

- **WHEN** the CyclesX distribution zip is built
- **THEN** the zip does not contain `blender_manifest.toml`

#### Scenario: HiFive and Eevee Next packages include the manifest

- **WHEN** the HiFive or Eevee Next distribution zip is built
- **THEN** the zip contains `blender_manifest.toml`
