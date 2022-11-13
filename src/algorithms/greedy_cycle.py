from src.model import DistanceMatrix, Node
from src.utils import get_edges, nodes_to_sequence


def greedy_cycle(
    pivot_node: Node, nodes: list[Node], node_coverage: int, distance_matrix: DistanceMatrix, **kwargs
) -> list[Node]:
    nodes_set = set(nodes)
    selected_nodes = [pivot_node]

    min_node = distance_matrix.get_nearest_node(pivot_node, set(nodes) - set(selected_nodes))

    pivot_node.add_connection(min_node)
    selected_nodes.append(min_node)

    anchor_nodes: tuple[Node, Node] | None = None
    for _ in range(node_coverage - 2):
        min_distance = float("inf")
        min_node = None

        edges = get_edges(selected_nodes)
        possible_nodes = nodes_set - set(selected_nodes)

        for node in possible_nodes:
            for edge in edges:
                distance = distance_matrix.get_node_to_edge_distance(node, edge)

                if distance < min_distance:
                    min_distance = distance
                    min_node = node
                    anchor_nodes = edge

        anchor_1, anchor_2 = anchor_nodes

        if len(selected_nodes) > 2:
            anchor_1.remove_connection(anchor_2)

        anchor_1.add_connection(min_node)
        anchor_2.add_connection(min_node)

        selected_nodes.append(min_node)

    return nodes_to_sequence(selected_nodes)
