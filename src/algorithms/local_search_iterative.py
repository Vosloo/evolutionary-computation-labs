from copy import deepcopy
from random import sample
from time import perf_counter

from src.algorithms import local_search_candidates, random_sequence
from src.model import DistanceMatrix, Node, Run
from src.utils import linked_to_sequence


def local_search_iterative(
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    no_candidates: int,
    max_runtime: float,
    **kwargs,
) -> list[Node]:
    del kwargs["initial_solution"]

    timer = perf_counter()
    nodes_set = set(nodes)

    random_sequence = random_sequence(deepcopy(nodes), **kwargs)
    current_sequence = local_search_candidates(
        initial_solution=random_sequence,
        nodes=nodes,
        distance_matrix=distance_matrix,
        no_candidates=no_candidates,
        **kwargs,
    )

    current_run = Run(current_sequence[0].id, current_sequence, distance_matrix)

    while True:
        # limit runtime by max_runtime
        if perf_counter() - timer > max_runtime:
            break

        new_sequence = _perturbation(deepcopy(current_sequence), nodes_set)
        new_sequence = local_search_candidates(
            initial_solution=new_sequence,
            nodes=nodes,
            distance_matrix=distance_matrix,
            no_candidates=no_candidates,
            **kwargs,
        )
        new_run = Run(new_sequence[0].id, new_sequence, distance_matrix)

        if new_run < current_run:
            current_run = new_run
            current_sequence = new_sequence

    return current_sequence


def _perturbation(selected_nodes: list[Node], nodes: set[Node]) -> list[Node]:
    perturbation_factor = 4
    sequence_nodes = set(selected_nodes)
    unsequenced_nodes = nodes - sequence_nodes

    old_nodes: list[Node] = sample(sequence_nodes, perturbation_factor)
    new_nodes: list[Node] = sample(unsequenced_nodes, perturbation_factor)

    for old_node, new_node in zip(old_nodes, new_nodes):
        prev_node, next_node = old_node.connections

        old_node.remove_connection(prev_node)
        old_node.remove_connection(next_node)

        new_node.add_prev_connection(prev_node)
        new_node.add_next_connection(next_node)

    return linked_to_sequence(new_nodes[-1])
