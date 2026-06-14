# Blender C&C Toolkit

An interactive Blender addon for generating template scenes used to render Command & Conquer game sprite assets.

## Addons

### HiFive (Blender 5.0+)

Full template scene generation with reactive rebuild. Operates from the 3D Viewport sidebar and mutates the active scene in-place. Supports all render types including Shadow with auto-calculated frame offsets for contiguous output.

### Eevee Next (Blender 4.2+)

Same feature set as HiFive, targeting Blender's EEVEE_NEXT engine. Provides the same workflow for users on Blender 4.2–4.x.

### CyclesX (Blender 3.0+)

Targets Blender 3.0's CyclesX engine. Includes engine-specific Cryptomatte handling, holdout plane occlusion fixes, and dedicated Denoise options panel.

## Features

- **Template Generation** — Camera, lighting, world HDRI, shadow/holdout planes, and compositor node tree configured per game
- **Games** — Red Alert 2, Tiberian Sun, ReWire, Red Alert / Tiberian Dawn, C&C Remastered, Dune 2000
- **Variants** — Base, Infantry, Effects (changes resolution, camera scale, lighting)
- **Render Types** — Default, Preview, Object, Buildup, Shadow
- **Render + Shadow** — Batch renders primary pass then Shadow pass with contiguous frame numbering
- **Shadow Controls** — Per-scene shadow color and opacity
- **Anti-aliasing** — Optional AA against background via compositor bypass
- **Transparent Background** — RGBA output with alpha channel control
- **Crop Canvas** — Configurable output dimensions
- **Background Image** — Optional reference image in Preview mode

## Installation

### From release zip

1. Download the `.zip` for your Blender version from [Releases](https://github.com/zawaro/blender-cnc-toolkit/releases)
2. In Blender: **Edit > Preferences > Add-ons > Install**
3. Select the downloaded `.zip`
4. Enable the addon in the list

### From source

Clone the repository and copy the addon folder into Blender's addons directory:

```bash
git clone https://github.com/zawaro/blender-cnc-toolkit.git
```

Copy `hi_five/` (Blender 5.0+), `eevee_next/` (Blender 4.2+), or `cyclesx/` (Blender 3.0+) into your Blender addons directory:

- **Linux:** `~/.config/blender/<version>/scripts/addons/`
- **macOS:** `~/Library/Application Support/Blender/<version>/scripts/addons/`
- **Windows:** `%APPDATA%\Blender Foundation\Blender\<version>\scripts\addons\`

Then enable the addon in **Edit > Preferences > Add-ons**.

## Usage

1. Open the **3D Viewport** sidebar (**N** key) and find the **C&C Toolkit** tab
2. Select a **Game**, **Variant**, and **Engine**
3. Click **Generate Template** to build the scene
4. Import your model into the scene
5. Switch between **Render Types** to preview different passes
6. Use **Render Current** for a single frame or **Render Animation** for the full sequence

### Render + Shadow

For Object and Buildup render types, enable **Render Shadow with Animation** to batch render the primary pass followed by the Shadow pass. Frame offsets are auto-calculated so output filenames are contiguous.

## Building

Build distribution zips with the included script:

```bash
./dist.sh
```

This will:
1. Create a virtual environment if needed (via [uv](https://docs.astral.sh/uv/))
2. Prompt you to select a toolkit (hi_five, eevee_next, cyclesx, or all)
3. Output versioned `.zip` files to `.dist/`

## License

GPL-3.0-or-later — see [LICENSE](LICENSE) for details.
