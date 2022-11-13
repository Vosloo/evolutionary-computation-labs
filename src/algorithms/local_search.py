from itertools import combinations, product
from random import shuffle

from src.model import DistanceMatrix, Node
from src.model import Run

def local_search(
    initial_solution: list[Node],
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    search_type: str,
    intra_type: str,
    **kwargs,
) -> list[Node]:
    nodes_set = set(nodes)

    current_run = Run(initial_solution[0].id, initial_solution, distance_matrix)

    while True:
        neighbourhood_inter = _inter(current_run.nodes, nodes_set)
        neighbourhood_intra = _intra(current_run.nodes, intra_type)

        if search_type == "steepest":
            neighbourhood = neighbourhood_inter + neighbourhood_intra
            neighbourhood = [
                Run(neighbour[0].id, neighbour, distance_matrix) for neighbour in neighbourhood
            ]

            if (new_run := min(neighbourhood)) < current_run:
                current_run = new_run
            else:
                break

        elif search_type == "greedy":
            neighbourhood = neighbourhood_inter + neighbourhood_intra
            starting_node = current_run.nodes[0]
            shuffle(neighbourhood)

            for neighbour in neighbourhood:
                new_run = Run(starting_node.id, neighbour, distance_matrix)
                if new_run < current_run:
                    current_run = new_run
                    break
            else:
                break

        else:
            raise ValueError("Invalid search_type")

    return current_run.nodes


def _inter(original_sequence: list[Node], nodes: set[Node]):
    og_seq = set(original_sequence)
    changes = product(og_seq, nodes - og_seq)

    neighbourhood = []
    for change in changes:
        from_node, to_node = change
        new_sequence = original_sequence.copy()

        from_ind = original_sequence.index(from_node)
        new_sequence[from_ind] = to_node

        neighbourhood.append(new_sequence)

    return neighbourhood


def _intra(original_sequence: list[Node], intra_type: str):
    if intra_type == "nodes":
        return _nodes_intra(original_sequence)
    elif intra_type == "edges":
        return _edges_intra(original_sequence)
    else:
        raise ValueError("Invalid intra_type")


def _edges_intra(original_sequence: list[Node]) -> list[list[Node]]:
    all_edges = [(i, i + 1) for i in range(len(original_sequence) - 1)]
    all_edges.append((len(original_sequence) - 1, 0))
    edge_swaps = list(combinations(all_edges, 2))

    # n*(n - 3)/2

    neighbourhood = []

    # remove non valid edge swaps
    for swap in edge_swaps:
        left, right = swap
        if left[1] == right[0] or left[0] == right[1]:
            continue

        shift = left[0]
        right_start_shifted = abs(right[0] - shift)

        shifted = original_sequence[shift:] + original_sequence[:shift]
        neighbourhood.append(
            shifted[:1] + shifted[right_start_shifted:0:-1] + shifted[right_start_shifted + 1 :]
        )

    return neighbourhood


def _nodes_intra(original_sequence: list[Node]) -> list[list[Node]]:
    # n*(n - 1)/2
    changes = set(combinations(original_sequence, 2))
    neighbourhood = []
    for change in changes:
        from_node, to_node = change
        new_sequence = original_sequence.copy()

        from_ind, to_ind = original_sequence.index(from_node), original_sequence.index(to_node)
        new_sequence[from_ind], new_sequence[to_ind] = to_node, from_node

        neighbourhood.append(new_sequence)

    return neighbourhood