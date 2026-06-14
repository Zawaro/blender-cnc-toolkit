import bpy


def arrange_nodes(node_trees: list[bpy.types.NodeTree]) -> None:
  for tree in node_trees:
    if not tree:
      continue
    nodes = tree.nodes
    if not nodes:
      continue

    groups = {}
    for node in nodes:
      group_key = node.location.y // 200
      groups.setdefault(group_key, []).append(node)

    sorted_groups = sorted(groups.items(), key=lambda item: item[0], reverse=True)
    for group_idx, (_, group_nodes) in enumerate(sorted_groups):
      y_pos = group_idx * 200
      sorted_in_group = sorted(group_nodes, key=lambda n: n.location.x)
      for node_idx, node in enumerate(sorted_in_group):
        node.location.x = node_idx * 400
        node.location.y = y_pos
