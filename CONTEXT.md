# Blender C&C Toolkit (HiFive)

An interactive Blender addon for generating template scenes used to render Command & Conquer game sprite assets. Operates from the 3D View sidebar and mutates the active scene in-place.

## Language

**Template scene**:
A Blender scene with camera, sun lighting, world HDRI, shadow-catching planes, holdout planes, and a compositor node tree pre-configured for rendering C&C game sprites. Applied by the addon and fully mutable.

**Variant**:
A game subtype (Base, Infantry, Effects) that changes resolution, camera ortho scale, sun position, and other scene parameters.

**Render type**:
One of Default, Preview, Object, Buildup, or Shadow — controls which planes are visible and how the compositor is wired.

**Render + Shadow**:
A batch operator that renders the primary pass (Object or Buildup) then the Shadow pass with auto-calculated frame offset so output filenames are contiguous.

**Frame Offset**:
A user-specified number added to output frame filenames for single-pass renders. For Render + Shadow the offset is auto-calculated.

**Anti-aliasing against background**:
When on, the compositor bypasses the Alpha Convert node group and uses Blender's native film_transparent alpha for smooth anti-aliased object edges.

**Transparent background**:
When on, the compositor outputs RGBA (alpha channel present) and prevents background colors/planes from passing to the rendered image. When off, outputs RGB with solid background color and all visible planes pass through.

**Full mutation**:
When the user changes game, variant, or engine, the template elements are deleted and rebuilt from scratch. User-imported objects outside the `_CNC_Toolkit` collection are preserved.

**Default** render type:
Shows only the grey reference plane against the scene background, no compositor processing. Used as the baseline state.

## Relationships

- A **Template scene** belongs to exactly one **Game** × **Variant** × **Engine** combination
- A **Render type** determines which template planes and compositor nodes are active
- **Render + Shadow** iterates over two render types with a **Frame Offset**
- **Anti-aliasing against background** and **Transparent background** modify the compositor output path

## Example dialogue

> **Dev:** "If the user changes from Red Alert 2 to Tiberian Sun, what happens to their imported model?"  
> **Domain expert:** "Nothing — the model is outside `_CNC_Toolkit`. Only the template elements (camera, lights, planes, world, compositor) get rebuilt."

> **Dev:** "So Render + Shadow would render Object frames 0-11 as `_0000.png` through `_0011.png`, then Shadow frames 0-11 as `_0012.png` through `_0023.png`?"  
> **Domain expert:** "Correct. The offset is auto-calculated from the scene frame range, so they land end-to-end in the output folder."
