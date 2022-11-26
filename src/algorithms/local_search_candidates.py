from src.model import Delta, DistanceMatrix, Node, Run


def local_search(
    initial_solution: list[Node],
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    no_candidates: int,
    **kwargs,
) -> list[Node]:
    if initial_solution is None:
        raise ValueError("Initial solution is None!")

    nodes_set = set(nodes)

    current_run = Run(0, initial_solution, distance_matrix)

    while True:
        if current_run.score < 0:
            raise ValueError("Initial solution is not valid!")

        neighbourhood: list[Delta] = _get_candidate_neighbourhood(current_run.nodes, no_candidates, distance_matrix)

        if (best_delta := min(neighbourhood)) < 0:
            current_run = Run.from_delta(current_run, best_delta)
        else:
            break

    return current_run.nodes


def _get_candidate_neighbourhood(
    original_sequence: list[Node],
    no_candidates: int,
    distance_matrix: DistanceMatrix,
) -> list[Delta]:
    og_seq = set(original_sequence)

    neighbourhood: list[Delta] = []
    for pivot_node in original_sequence:
        neighbours = distance_matrix.get_n_nearest_nodes(pivot_node, no_candidates)
        for neighbour in neighbours:
            if neighbour in og_seq:
                # DeltaCandidateEdges
                ...
            else:
                # DeltaCandidateNodes
                neighbourhood.extend(_inter(pivot_node, neighbour))

    return neighbourhood

def _inter(pivot_node: Node, neighbour: Node) -> list[DeltaInterNodes]:
    pivot_node.next_connection
    neighbour
    Delta()

    pivot_node.prev_connection
    neighbour
    Delta()

    return [delta1, delta2]

    # 1 2 3 4 5 6 7

    # (2 , 6)

    # 1 2 5 6

    # 2 3 6 7

    # 5 6 7 1 2 3 4
    # 5 1 7 6 2 3 4
