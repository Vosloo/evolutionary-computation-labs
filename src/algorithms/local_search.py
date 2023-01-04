from copy import deepcopy
from itertools import combinations, product

import numpy as np

from src.model import (
    Delta,
    DeltaInterNodes,
    DeltaIntraEdges,
    DeltaIntraNodes,
    DistanceMatrix,
    Node,
    Run,
)
from src.utils import get_edges
from src.algorithms import random_sequence

def local_search(
    initial_solution: list[Node],
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    search_type: str,
    intra_type: str,
    **kwargs,
) -> list[Node]:
    if initial_solution is None:
        initial_solution = random_sequence(deepcopy(nodes), **kwargs)

    nodes_set = set(nodes)

    current_run = Run(0, initial_solution, distance_matrix)

    while True:
        if current_run.score < 0:
            raise ValueError("Initial solution is not valid!")

        neighbourhood_inter = _inter(current_run.nodes, nodes_set, distance_matrix)
        neighbourhood_intra = _intra(current_run.nodes, intra_type, distance_matrix)
        neighbourhood: list[Delta] = neighbourhood_inter + neighbourhood_intra

        if search_type == "steepest":
            if (best_delta := min(neighbourhood)) < 0:
                current_run = Run.from_delta(current_run, best_delta)
            else:
                break

        elif search_type == "greedy":
            np.random.shuffle(neighbourhood)

            for delta in neighbourhood:
                if delta < 0:
                    current_run = Run.from_delta(current_run, delta)
                    break
            else:
                break

        else:
            raise ValueError("Invalid search_type")

    return current_run.nodes


def _inter(
    original_sequence: list[Node], nodes: set[Node], distance_matrix: DistanceMatrix
) -> list[DeltaInterNodes]:
    og_seq = set(original_sequence)
    changes = product(og_seq, nodes - og_seq)

    neighbourhood: list[DeltaInterNodes] = []
    for change in changes:
        inter_node, outer_node = change
        neighbourhood.append(DeltaInterNodes(inter_node, outer_node, distance_matrix))

    return neighbourhood


def _intra(
    original_sequence: list[Node], intra_type: str, distance_matrix: DistanceMatrix
) -> list[DeltaIntraNodes] | list[DeltaIntraEdges]:
    if intra_type == "nodes":
        return _nodes_intra(original_sequence, distance_matrix)
    elif intra_type == "edges":
        return _edges_intra(original_sequence, distance_matrix)
    else:
        raise ValueError("Invalid intra_type")


def _edges_intra(
    original_sequence: list[Node], distance_matrix: DistanceMatrix
) -> list[DeltaIntraEdges]:
    all_edges = get_edges(original_sequence)
    edge_swaps = combinations(all_edges, 2)

    neighbourhood = []

    # remove non valid edge swaps
    for swap in edge_swaps:
        left, right = swap
        if left[1] == right[0] or left[0] == right[1]:
            continue

        outerA, outerB = left[0], right[1]

        neighbourhood.append(DeltaIntraEdges(outerA, outerB, distance_matrix))

    # Size: n*(n - 3)/2
    return neighbourhood


def _nodes_intra(
    original_sequence: list[Node], distance_matrix: DistanceMatrix
) -> list[DeltaIntraNodes]:
    changes = combinations(original_sequence, 2)
    neighbourhood = []
    for change in changes:
        from_node, to_node = change
        neighbourhood.append(DeltaIntraNodes(from_node, to_node, distance_matrix))

    # Size: n*(n - 1)/2
    return neighbourhood
