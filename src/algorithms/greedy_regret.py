from src.model import DistanceMatrix, Node
from src.utils import get_edges, linked_to_sequence

import numpy as np


def greedy_regret(
    pivot_node: Node,
    nodes: list[Node],
    node_coverage: int,
    distance_matrix: DistanceMatrix,
    k_regret: int,
    regret_weights: tuple[float, float] | None = None,
    **kwargs
) -> list[Node]:
    nodes_set = set(nodes)
    selected_nodes = [pivot_node]

    # Selecting 3 starting nodes for greedy regret using nearest neighbour algorithm
    for _ in range(2):
        pivot_node = selected_nodes[-1]
        min_node = distance_matrix.get_nearest_node(pivot_node, set(nodes) - set(selected_nodes))

        pivot_node.add_next_connection(min_node)
        selected_nodes.append(min_node)

    selected_nodes[-1].add_next_connection(selected_nodes[0])

    for _ in range(node_coverage - len(selected_nodes)):
        min_node = None
        edges = get_edges(selected_nodes)

        possible_nodes = nodes_set - set(selected_nodes)
        nodes_distances = np.array(
            [
                [distance_matrix.get_node_to_edge_distance(node, edge) for edge in edges]
                for node in possible_nodes
            ]
        )

        nodes_distances_edges = np.argsort(nodes_distances, axis=1)
        nodes_distances = np.take_along_axis(nodes_distances, nodes_distances_edges, axis=1)
        k_best = nodes_distances[:, :k_regret]

        regrets = k_best[:, 0] - k_best[:, 1]

        if regret_weights is not None:
            regrets = (regrets * regret_weights[0]) + (regret_weights[1] * k_best[:, 0])

        chosen_ind = np.argmin(regrets)
        chosen_edge_ind = nodes_distances_edges[chosen_ind, 0]

        min_node = list(possible_nodes)[chosen_ind]
        anchor_1, anchor_2 = edges[chosen_edge_ind]

        if len(selected_nodes) > 2:
            anchor_1.remove_connection(anchor_2)

        if anchor_1.prev_connection is None:
            anchor_1.add_prev_connection(min_node)
            anchor_2.add_next_connection(min_node)
        else:
            anchor_1.add_next_connection(min_node)
            anchor_2.add_prev_connection(min_node)

        selected_nodes.append(min_node)

    return linked_to_sequence(selected_nodes[0])
