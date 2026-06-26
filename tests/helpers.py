def get_compositor_tree(scene):
  if hasattr(scene, "compositing_node_group") and scene.compositing_node_group:
    return scene.compositing_node_group
  if getattr(scene, "use_nodes", False) and getattr(scene, "node_tree", None):
    return scene.node_tree
  return None
