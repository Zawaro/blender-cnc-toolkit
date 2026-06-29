# Changelog

## [0.3.1](https://github.com/Zawaro/blender-cnc-toolkit/compare/v0.3.0...v0.3.1) (2026-06-29)


### Features

* darken shadows — reduce bounces to 0, desaturate sky, config-driven air_density ([7b0937a](https://github.com/Zawaro/blender-cnc-toolkit/commit/7b0937af8c94a64d299b0be4ad13efaa5cf8a933)), closes [#30](https://github.com/Zawaro/blender-cnc-toolkit/issues/30)
* set Cycles adaptive_threshold to 0.001 for sharper renders ([d5dbb79](https://github.com/Zawaro/blender-cnc-toolkit/commit/d5dbb79d9df488bd276844e539a3d9977fdaedf8))


### Bug Fixes

* add missing cyclesx/blender_manifest.toml to extra-files ([05fc3fa](https://github.com/Zawaro/blender-cnc-toolkit/commit/05fc3fa3b69a6ef56e0f7b10f0e08486ef1551df))
* add x-release-please-version annotations for version sync ([11b4f78](https://github.com/Zawaro/blender-cnc-toolkit/commit/11b4f784c43498c10321f2fd2eca04989030cbf6))
* disable Cycles denoising — causes blurry renders ([b81ce1c](https://github.com/Zawaro/blender-cnc-toolkit/commit/b81ce1c28685a0f6ba1ddff30d300b96718c5aac))
* pass rl node to _create_remap_hue in cyclesx _wire_ac_ao ([f2bd0f6](https://github.com/Zawaro/blender-cnc-toolkit/commit/f2bd0f62d1e8d51245b989bf2126f6d0ab4d1b76))
* read version from version.txt directly, remove sync workflow ([5737cf5](https://github.com/Zawaro/blender-cnc-toolkit/commit/5737cf522678a52cdf7fbc9e25647c3b59feac0e))
* rename commitlint config to .cjs for ESM compatibility ([02b0a66](https://github.com/Zawaro/blender-cnc-toolkit/commit/02b0a662db257fd16510b4f2e330953c5986ec01))
* revert __init__.py to static bl_info, fix version sync ([e30f2d2](https://github.com/Zawaro/blender-cnc-toolkit/commit/e30f2d2c411bdb4eb507331dfccfaf14d529ff01))
* specify commitlint config file path ([a60109f](https://github.com/Zawaro/blender-cnc-toolkit/commit/a60109f6c3580a61e70fa6fd08eb78a99efcecc5))
* sync bl_info version via workflow instead of broken annotation ([46176f9](https://github.com/Zawaro/blender-cnc-toolkit/commit/46176f9e824b37045f00133d92fd5adc3937e8c7))
* syntax error in cyclesx _wire_object_or_buildup + restore tomli fallback ([f908c1e](https://github.com/Zawaro/blender-cnc-toolkit/commit/f908c1e4fcffb8e2419f5be147477ca2680f8986))
* use group-pull-request-title-pattern for grouped release PRs ([286d7ad](https://github.com/Zawaro/blender-cnc-toolkit/commit/286d7ad2e7be1b15ccd01133ec4000d879cb545d))
