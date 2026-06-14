# ADR-0001: Interactive addon architecture with in-place scene mutation

The toolkit is built as a live Blender addon (property update callbacks mutate the active scene in real time) rather than a build-time script that generates `.blend` files.

**Context**: The predecessor project (`blender-cnc-templates`) generates `.blend` files headlessly at build time, baking 21 pre-configured scenes into each file. Artists then open the file and run text-block scripts to switch between render types. This approach is powerful for distribution but inflexible during iteration — changing a single value (e.g. background color) requires editing the build script and rebuilding the entire `.blend`.

**Decision**: Build the HiFive variant as an interactive Blender addon that mutates the active scene in-place via property update callbacks. Each UI change tears down and rebuilds the relevant scene elements (compositor, plane visibility, world, camera, lights) from scratch.

**Trade-offs**: The live approach gives instant feedback but requires more complex state management (save/restore on generate/purge, careful resource cleanup to avoid orphaned data blocks). The build-time approach is simpler but has a edit-rebuild-reload cycle for any change. For a toolkit aimed at active sprite production where artists need to tweak settings per-session, the interactive trade-off is correct.
