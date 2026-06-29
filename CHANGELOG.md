# Changelog

## [0.3.1](https://github.com/Zawaro/blender-cnc-toolkit/compare/v0.3.0...v0.3.1) (2026-06-29)


### Features

* darken shadows — reduce bounces to 0, desaturate sky, config-driven air_density ([7b0937a](https://github.com/Zawaro/blender-cnc-toolkit/commit/7b0937af8c94a64d299b0be4ad13efaa5cf8a933)), closes [#30](https://github.com/Zawaro/blender-cnc-toolkit/issues/30)
* set Cycles adaptive_threshold to 0.001 for sharper renders ([d5dbb79](https://github.com/Zawaro/blender-cnc-toolkit/commit/d5dbb79d9df488bd276844e539a3d9977fdaedf8))


### Bug Fixes

* disable Cycles denoising — causes blurry renders ([b81ce1c](https://github.com/Zawaro/blender-cnc-toolkit/commit/b81ce1c28685a0f6ba1ddff30d300b96718c5aac))
* pass rl node to _create_remap_hue in cyclesx _wire_ac_ao ([f2bd0f6](https://github.com/Zawaro/blender-cnc-toolkit/commit/f2bd0f62d1e8d51245b989bf2126f6d0ab4d1b76))
* rename commitlint config to .cjs for ESM compatibility ([02b0a66](https://github.com/Zawaro/blender-cnc-toolkit/commit/02b0a662db257fd16510b4f2e330953c5986ec01))
* specify commitlint config file path ([a60109f](https://github.com/Zawaro/blender-cnc-toolkit/commit/a60109f6c3580a61e70fa6fd08eb78a99efcecc5))
* syntax error in cyclesx _wire_object_or_buildup + restore tomli fallback ([f908c1e](https://github.com/Zawaro/blender-cnc-toolkit/commit/f908c1e4fcffb8e2419f5be147477ca2680f8986))
