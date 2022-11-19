from src.model import DistanceMatrix, Node
from src.utils import sort_connections


def nearest(
    pivot_node: Node, nodes: list[Node], node_coverage: int, distance_matrix: DistanceMatrix, **kwargs
) -> list[Node]:
    nodes_set = set(nodes)
    selected_nodes = [pivot_node]

    for _ in range(node_coverage - 1):
        curr_node = selected_nodes[-1]
        unselected_nodes = nodes_set - set(selected_nodes)

        min_node = distance_matrix.get_nearest_node(curr_node, unselected_nodes)

        selected_nodes.append(min_node)

    return sort_connections(selected_nodes)
