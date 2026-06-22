# Blender C&C Toolkit — Usage Guide

## Introduction

The Blender C&C Toolkit is an addon for generating template scenes used to render
Command & Conquer game sprite assets. It sets up cameras, lighting, world HDRI,
shadow/holdout planes, and compositor node trees so you can focus on importing your
model and rendering.

Supported games: Red Alert 2, Tiberian Sun, ReWire, Red Alert / Tiberian Dawn,
C&C Remastered, Dune 2000.


## Installation

1. Download the `.zip` for your Blender version from
   [Releases](https://github.com/zawaro/blender-cnc-toolkit/releases)
2. In Blender: **Edit > Preferences > Add-ons > Install**
3. Select the downloaded `.zip`
4. Enable the addon in the list

For source installation, see the README on
[GitHub](https://github.com/zawaro/blender-cnc-toolkit).


## Quick Start

1. Open the **3D Viewport** sidebar by pressing **N**
2. Find the **C&C Toolkit** tab
3. Select a **Game**, **Variant**, and **Engine**
4. Click **Generate Template**
5. Import your 3D model into the scene
6. Switch between **Render Types** to preview different passes
7. Use **Render Current** for a single frame or **Render Animation** for the full
   sequence


## Settings Reference

### Game

| Value                       | Description            |
|-----------------------------|------------------------|
| Red Alert 2                 | RA2 sprites            |
| Tiberian Sun                | TS sprites             |
| ReWire                      | RW sprites             |
| Red Alert / Tiberian Dawn   | RA1 sprites            |
| C&C Remastered              | RM sprites             |
| Dune 2000                   | D2K sprites            |

### Variant

| Value    | Description                                          |
|----------|------------------------------------------------------|
| Base     | Standard building/unit sprites                       |
| Infantry | Infantry-sized sprites (smaller resolution/camera)   |
| Effects  | Explosion/effect sprites                             |

### Engine

| Value  | Description                                   |
|--------|-----------------------------------------------|
| Cycles | Path tracer — higher quality, slower          |
| Eevee  | Real-time — faster, good for preview          |

### Camera Mode

Available for RA1, RM, and D2K games.

| Value       | Description                               |
|-------------|-------------------------------------------|
| Perspective | Original 3D perspective camera view       |
| Isometric   | Standard C&C isometric camera view        |


## Render Types

Each render type configures which planes and effects are visible.

| Type         | Use case                                                                                                           |
|--------------|--------------------------------------------------------------------------------------------------------------------|
| **Default**  | Standard sprite render with grey background. Good for final output when you want a solid background.               |
| **Preview**  | Full preview with holdout planes, shadow, and ambient occlusion. Use this to see how the sprite will look in-game. |
| **Object**   | Ambient occlusion pass. The grey background plane is hidden — useful for compositing with your own background.     |
| **Buildup**  | Shadow catcher variant. Renders with a secondary shadow catcher plane for buildup animation frames.                |
| **Shadow**   | Shadow-only pass. Renders just the shadow for compositing onto other frames.                                       |


## Render + Shadow Workflow

For Object and Buildup render types, you can enable **Render shadow with animation**
to batch render the primary pass followed by the Shadow pass in one go.

How it works:
1. Enable **Render shadow with animation** in the panel
2. Click **Render Animation**
3. The primary pass renders all frames first
4. Then the Shadow pass renders all frames
5. Frame offsets are auto-calculated so output filenames are contiguous

Example output with 10 frames:
- Primary pass: `render_0000.png` through `render_0009.png`
- Shadow pass: `render_0010.png` through `render_0019.png`

This makes it easy to combine passes in your game engine or compositing software.


## Background & Colors

### Background Color

Sets the solid background color for non-transparent renders. Only visible when
**Transparent background** is off.

### Shadow Color

Color tint applied to shadow-only renders. The shadow plane picks up this color
instead of pure black.

### Shadow Opacity

Controls the opacity of the shadow tint. Only available in Preview render type.
Set to 0 for no shadow, 1 for full shadow.

### Transparent Background

When enabled, outputs RGBA images with an alpha channel. When off, outputs RGB
with the solid background color.

### Anti-aliasing against Background

Bypasses the Alpha Convert node group for smooth anti-aliased edges against the
background. Enable this if you notice jagged edges on your sprites.


## Crop Canvas

The Crop Canvas feature lets you set custom output dimensions independent of the
game's default resolution.

1. Find the **Crop Canvas** sub-panel in the sidebar
2. Enable the checkbox
3. Set **X** and **Y** dimensions in pixels

This is useful when you need non-standard sprite sizes or want to add padding
around your render.


## Material Remapping

Material remapping lets you shift the hue of specific materials in your scene.
This is useful for creating color variants of the same sprite.

1. Select a material in the viewport
2. Use the material picker in the **Remap Materials** section
3. Click **Add**
4. Set the target **Remap Color** (the hue you want to shift to)
5. The material will be remapped when you regenerate or rebuild the template

To remove a material from the remap list, click the **X** button next to it.
To clear all remapped materials, click **Clear All**.


## Tips

### Cell Heights

The Z coordinates for C&C cell heights:

| Cell | Z (Blender Units)             |
|------|-------------------------------|
| 0    | 0.0                           |
| 1    | 0.816625                      |
| 2    | 1.63325                       |
| 3    | 2.449875                      |
| 4    | 3.2665 (default cliff height) |

### Render Quality

To improve render quality, go to the **Render** tab in Blender's Properties panel
and increase the **Sampling > Render** value. The default is set for fast renders;
try 100 or higher for production quality.

### GPU Rendering

If you have a compatible GPU, enable it in **Edit > Preferences > System** for
faster renders with Cycles.

### Tile Size (CPU rendering)

When rendering on CPU, set **Performance > Tile Size** to 16x16 for optimal speed.
