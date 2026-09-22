# distribution Specification

## Purpose
The dist.py packaging pipeline: versioned zips, version baking and restoration, build number, generated metadata, and file exclusions. Terms: Distribution build.
## Requirements
### Requirement: Distribution build
The toolkit SHALL provide a build command that packages a variant's addon directory into a versioned zip in the distribution directory.

#### Scenario: A variant is packaged

- **WHEN** a variant is built
- **THEN** a zip containing that addon's files is written to the distribution directory

#### Scenario: All variants are packaged

- **WHEN** the all-variants build is run
- **THEN** a zip is written for each of HiFive, Eevee Next, and CyclesX

### Requirement: Version baking and restoration
During packaging the build SHALL bake the source-of-truth version into the addon's `bl_info` version tuple, and SHALL restore the original `__init__.py` afterwards.

#### Scenario: Version is baked into the zip

- **WHEN** a variant is packaged from source version `0.3.0`
- **THEN** the packaged `__init__.py` declares version `(0, 3, 0)`

#### Scenario: Source is restored after packaging

- **WHEN** packaging finishes
- **THEN** the source `__init__.py` is restored to its original content

### Requirement: Build number
The build SHALL include a build number derived from the repository's total git commit count, falling back to `"0"` when that count is unavailable.

#### Scenario: Build number from git

- **WHEN** the repository history is available
- **THEN** the build number is the total commit count

#### Scenario: Build number fallback

- **WHEN** the git commit count cannot be determined
- **THEN** the build number is `"0"`

### Requirement: Generated build metadata
Packaging SHALL write a generated build module containing the build number into the packaged addon, and SHALL remove that generated module from the source directory after packaging.

#### Scenario: Build module is packaged

- **WHEN** a variant is packaged
- **THEN** the zip contains a generated build module declaring the build number

#### Scenario: Build module is cleaned up

- **WHEN** packaging finishes
- **THEN** the generated build module no longer exists in the source addon directory

### Requirement: Build file exclusions
Packaging SHALL exclude development and cache directories from the zip, including virtual environments, bytecode caches, git data, and documentation.

#### Scenario: Development directories are excluded

- **WHEN** a variant is packaged
- **THEN** virtual environments, bytecode caches, git data, and documentation are not included in the zip
