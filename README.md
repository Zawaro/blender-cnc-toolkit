# Blender C&C Toolkit

An interactive Blender addon for generating template scenes used to render Command & Conquer game sprite assets.

## Addons

| Blender | Folder | Notes |
|---------|--------|-------|
| 5.0+ | `hi_five` | Latest stable release |
| 4.2–4.x | `eevee_next` | Eevee Next engine |
| 3.0–3.6 | `cyclesx` | Cycles X engine |

All three addons share the same feature set and UI. They differ only in Blender version compatibility and render engine support.

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
./dist.sh              # interactive prompt
python dist.py --all   # all variants
python dist.py --variant hi_five  # single variant
```

Output: `.dist/<variant>_<version>_build<N>.zip`

## Releasing

This project uses [release-please](https://github.com/googleapis/release-please) for automated releases. PR titles and commit messages must follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add new feature` → minor version bump
- `fix: resolve bug` → patch version bump
- `feat!: breaking change` → major version bump

When a Release PR merges, GitHub Actions builds all variants, creates a GitHub Release with zips attached, and tags with build number (`v0.4.0_build37`).

## Development

### Setup

```bash
git clone https://github.com/zawaro/blender-cnc-toolkit.git
cd blender-cnc-toolkit
uv sync --group test --group dev
uv run pre-commit install
```

### Testing

Tests run inside Blender's headless Python using [pytest-blender](https://github.com/mondeja/pytest-blender):

```bash
# Single variant
BLENDER_EXECUTABLE=/path/to/blender ./test.sh

# All variants (set paths in .env first)
cp .env.example .env   # edit with your Blender paths
./test.sh --all

# Or run pytest directly
BLENDER_ADDON=hi_five BLENDER_EXECUTABLE=/path/to/blender uv run pytest --blender-addons-dirs . -v -- -noaudio
```

`.env` maps addon variants to local Blender executables:
- `BLENDER_5` → hi_five (Blender 5.0+)
- `BLENDER_4` → eevee_next (Blender 4.2–4.x)
- `BLENDER_3` → cyclesx (Blender 3.0–3.6)

Each Blender's Python needs pytest installed: `<blender>/python/bin/python3.XX -m pip install pytest`

### Pre-commit

Pre-commit hooks run ruff linting and formatting on every commit:

```bash
uv run pre-commit run --all-files
```

## License

GPL-3.0-or-later — see [LICENSE](LICENSE) for details.
