from src.model import Delta, DeltaCandidateNodes, DistanceMatrix, Node, Run, DeltaCandidateEdges


def local_search_candidates(
    initial_solution: list[Node],
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    no_candidates: int,
    **kwargs,
) -> list[Node]:
    if initial_solution is None:
        raise ValueError("Initial solution is None!")

    current_run = Run(0, initial_solution, distance_matrix)

    while True:
        if current_run.score < 0:
            raise ValueError("Initial solution is not valid!")

        neighbourhood: list[Delta] = _get_candidate_neighbourhood(
            current_run.nodes, nodes, no_candidates, distance_matrix
        )

        if (best_delta := min(neighbourhood)) < 0:
            current_run = Run.from_delta(current_run, best_delta)
        else:
            break

    return current_run.nodes


def _get_candidate_neighbourhood(
    original_sequence: list[Node],
    nodes: list[Node],
    no_candidates: int,
    distance_matrix: DistanceMatrix,
) -> list[Delta]:
    seq_dict = {node.id: node for node in original_sequence}

    neighbourhood: list[Delta] = []
    for pivot_node in original_sequence:
        neighbour_idx = distance_matrix.get_n_nearest_nodes_indices(pivot_node, no_candidates)
        for neighbour_ind in neighbour_idx:
            if neighbour_ind in seq_dict:
                # DeltaCandidateEdges
                neighbour = seq_dict[neighbour_ind]
                neighbourhood.extend(_intra(pivot_node, neighbour, distance_matrix))
            else:
                # DeltaCandidateNodes
                neighbour = nodes[neighbour_ind]
                neighbourhood.append(_inter(pivot_node, neighbour, distance_matrix))

    return neighbourhood


def _intra(
    pivot_node: Node, neighbour: Node, distance_matrix: DistanceMatrix
) -> list[DeltaCandidateEdges]:
    return [
        DeltaCandidateEdges(pivot_node, neighbour, distance_matrix, is_next=True),
        DeltaCandidateEdges(pivot_node, neighbour, distance_matrix, is_next=False),
    ]


def _inter(pivot_node: Node, neighbour: Node, distance_matrix: DistanceMatrix) -> DeltaCandidateNodes:
    return DeltaCandidateNodes(pivot_node, neighbour, distance_matrix)
