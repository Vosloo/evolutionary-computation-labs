from copy import deepcopy
from random import sample
from time import perf_counter

from src.algorithms import local_search_candidates, random_sequence
from src.model import DistanceMatrix, Node, Run
from src.utils import linked_to_sequence, validate_sequence


def local_search_iterative(
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    no_candidates: int,
    max_runtime: float,
    **kwargs,
) -> list[Node]:
    """Iterative local search algorithm.

    Args:
        nodes (list[Node]): List of nodes to be sequenced.
        distance_matrix (DistanceMatrix): Distance matrix.
        no_candidates (int): Number of candidates to be generated.
        max_runtime (float): Maximum runtime in seconds.

    Returns:
        list[Node]: Sequence of nodes.
    """
    del kwargs["initial_solution"]

    timer = perf_counter()
    nodes_set = set(nodes)

    current_sequence = random_sequence(deepcopy(nodes), **kwargs)

    print("\nIs random sequence valid?", validate_sequence(current_sequence))
    current_sequence = local_search_candidates(
        initial_solution=current_sequence,
        nodes=deepcopy(nodes),
        distance_matrix=distance_matrix,
        no_candidates=no_candidates,
        **kwargs,
    )
    print("Is pre-loop local search sequence valid?", validate_sequence(current_sequence))

    current_run = Run(current_sequence[0].id, current_sequence, distance_matrix)

    while True:
        # limit runtime by max_runtime
        if perf_counter() - timer > max_runtime:
            break

        new_sequence = _perturbation(deepcopy(current_sequence), nodes_set)
        print("Is perturbation sequence valid?", validate_sequence(new_sequence))

        new_sequence = local_search_candidates(
            initial_solution=new_sequence,
            nodes=deepcopy(nodes),
            distance_matrix=distance_matrix,
            no_candidates=no_candidates,
            **kwargs,
        )
        print("Is post-loop local search sequence valid?", validate_sequence(new_sequence))

        new_run = Run(new_sequence[0].id, new_sequence, distance_matrix)

        if new_run < current_run:
            current_run = new_run
            current_sequence = new_sequence

    return current_sequence


def _perturbation(selected_nodes: list[Node], nodes: set[Node]) -> list[Node]:
    print("Perturbation")
    perturbation_factor = 4
    sequence_nodes = set(selected_nodes)
    unsequenced_nodes = nodes - sequence_nodes

    print(
        f"sequence_nodes.intersection(unsequenced_nodes): {sequence_nodes.intersection(unsequenced_nodes)}"
    )

    if len(sequence_nodes) < perturbation_factor:
        raise ValueError("Perturbation factor cannnot be larger than the number of sequenced nodes")

    if len(unsequenced_nodes) < perturbation_factor:
        raise ValueError("Perturbation factor cannnot be larger than the number of unsequenced nodes")

    old_nodes: list[Node] = sample(sequence_nodes, perturbation_factor)
    new_nodes: list[Node] = sample(unsequenced_nodes, perturbation_factor)

    print(f"old_nodes: {old_nodes}")
    print(f"Any old is in unsequenced: {any([node in unsequenced_nodes for node in old_nodes])}")
    print(f"new_nodes: {new_nodes}")
    print(f"Any new is in sequenced: {any([node in sequence_nodes for node in new_nodes])}")

    if any([node.id == 30 for node in old_nodes]) or any([node.id == 30 for node in new_nodes]):
        pass

    # 1 2 _ 4 5 6 7
    for old_node, new_node in zip(old_nodes, new_nodes):
        prev_node, next_node = old_node.connections

        old_node.remove_connection(prev_node)
        new_node.add_prev_connection(prev_node)

        old_node.remove_connection(next_node)
        new_node.add_next_connection(next_node)

        ind = selected_nodes.index(old_node)
        selected_nodes[ind] = new_node

    return selected_nodes
    # return linked_to_sequence(new_nodes[-1])
