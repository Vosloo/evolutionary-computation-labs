from copy import deepcopy
from random import random, sample
from time import perf_counter
import numpy as np

from src.algorithms import local_search, random_sequence, greedy_regret
from src.model import DistanceMatrix, Node, Run

from src.utils import get_edges, linked_to_sequence


def local_search_LSN(
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    max_runtime: float,
    is_local_search_enabled: bool,
    **kwargs,
) -> list[Node]:
    del kwargs["initial_solution"]

    timer = perf_counter()
    current_sequence = random_sequence(deepcopy(nodes), **kwargs)

    if is_local_search_enabled:
        current_sequence = local_search(
            current_sequence,
            deepcopy(nodes),
            distance_matrix,
            search_type="steepest",
            intra_type="edges",
            **kwargs,
        )

    current_run = Run(current_sequence[0].id, current_sequence, distance_matrix)

    nodes_set = set(nodes)
    counter = -1
    while True:
        counter += 1
        if perf_counter() - timer > max_runtime:
            break

        new_sequence = destroy(deepcopy(current_sequence))
        new_sequence = repair(deepcopy(new_sequence), deepcopy(nodes_set), distance_matrix, **kwargs)

        if is_local_search_enabled:
            new_sequence = local_search(
                new_sequence, deepcopy(nodes), distance_matrix, search_type="steepest", intra_type="edges"
            )

        new_run = Run(new_sequence[0].id, new_sequence, distance_matrix)

        if new_run < current_run:
            current_run = new_run
            current_sequence = new_sequence

    print(f"\nNo. runs: {counter}")
    return current_sequence


def destroy(current_sequence: list[Node]):
    """
    Randomly destroys 20-30% (chosen randomly) of the sequence and returns the new sequence
    """
    multiplier = 0.2 + round(random()) * 0.1
    nodes_to_delete = sample(current_sequence, int(len(current_sequence) * multiplier))

    for node in nodes_to_delete:
        prev_node, next_node = node.prev_connection, node.next_connection

        node.remove_connection(prev_node).remove_connection(next_node)
        prev_node.add_next_connection(next_node)

    if prev_node is None:
        raise ValueError("prev_node is None")

    return linked_to_sequence(prev_node)


def repair(
    current_sequence: list[Node],
    nodes_set: set[Node],
    distance_matrix: DistanceMatrix,
    **kwargs,
) -> list[Node]:
    """
    Repairs the sequence by running greedy-regret
    """
    return greedy_regret(current_sequence, nodes_set, distance_matrix, **kwargs)


def greedy_regret(
    selected_nodes: list[Node],
    nodes_set: set[Node],
    distance_matrix: DistanceMatrix,
    node_coverage: int,
    k_regret: int,
    regret_weights: tuple[float, float],
    **kwargs,
) -> list[Node]:
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
