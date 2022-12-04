from src.algorithms import local_search_moves, random
from src.model import DistanceMatrix, Node, Run


def local_search_MSLS(
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    no_iterations: int,
    **kwargs,
) -> list[Node]:
    """Local Search with Multi-Start Local Search

    Args:
        nodes (list[Node]): list of nodes
        distance_matrix (DistanceMatrix): distance matrix
        no_iterations (int): number of iterations

    Returns:
        list[Node]: list of nodes
    """
    del kwargs["initial_solution"]

    nodes_runs: list[list[Node]] = []
    for _ in range(no_iterations):
        print(f"\r{_ + 1:3} / {no_iterations:3}", end="")
        initial_solution = random(nodes, **kwargs)
        nodes_runs.append(
            local_search_moves(
                initial_solution=initial_solution,
                nodes=nodes,
                distance_matrix=distance_matrix,
                **kwargs,
            )
        )

    runs = [Run(selected_nodes[0].id, selected_nodes, distance_matrix) for selected_nodes in nodes_runs]
    return min(runs)._selected_nodes

