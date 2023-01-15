from copy import deepcopy
from random import choice, sample
from numpy.random import shuffle
from time import perf_counter

from src.algorithms import local_search_candidates
from src.algorithms.local_search_LSN import repair
from src.model import DistanceMatrix, Node, Run
from src.model.enum import Operator
from src.utils import linked_to_sequence


def hybrid_evolution(
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    max_runtime: float,
    population_size: int,
    operator: Operator,
    is_local_search_enabled: bool,
    initial_runs: dict[str, list[Run]],
    instance_name: str,
    **kwargs,
) -> list[Node]:
    # set different id for each run to help keep track
    current_id = 0

    population, current_id = generate_initial_population(
        initial_runs[instance_name], population_size, current_id, distance_matrix
    )

    timer = perf_counter()

    while True:
        if perf_counter() - timer > max_runtime:
            break

        # select parents
        parents = sample(list(population.values()), k=2)

        # generate offspring
        offspring: Run = generate_offspring(
            parents, current_id, operator, deepcopy(nodes), distance_matrix, **kwargs
        )
        current_id += 1

        # perform local search on offspring
        if is_local_search_enabled:
            offspring_nodes = local_search_candidates(
                initial_solution=offspring.nodes,
                nodes=deepcopy(nodes),
                distance_matrix=distance_matrix,
                no_candidates=10,
            )

            offspring = Run(offspring.id, offspring_nodes, distance_matrix)

        # add offspring to population
        population[offspring.id] = offspring

        # remove non-unique solutions
        non_unique = _get_non_unique_solutions(population)
        if len(non_unique) == 1:
            if offspring.id == non_unique[0]:
                del population[offspring.id]
            else:
                raise Exception("Found single non-unique solution, but it's not the offspring")
        elif len(non_unique) > 1:
            raise Exception("More than one non-unique solution found")
        else:
            # if there is no non-unique solutions, remove the worst solution
            worse_solution = max(population.values())
            del population[worse_solution.id]

    return min(population.values())._selected_nodes


def _get_non_unique_solutions(population: dict[int, Run]) -> list[int]:
    """Returns a list of ids of non-unique solutions"""

    non_unique = []
    unique_scores = set()

    for run in population.values():
        if run.score in unique_scores:
            non_unique.append(run.id)
        else:
            unique_scores.add(run.score)

    return non_unique


def _operator1(
    parents: list[Run], current_id: int, nodes: list[Node], distance_matrix: DistanceMatrix, **kwargs
) -> Run:
    nodes_map = {node.id: node for node in deepcopy(nodes)}

    parentA_nodes = parents[0].nodes
    parentB_nodes = parents[1].nodes

    common_nodes = set(parentA_nodes).intersection(set(parentB_nodes))
    random_nodes = list(set(deepcopy(nodes)).difference(common_nodes))
    shuffle(random_nodes)

    offspring_nodes: list[Node] = []

    for ind, node in enumerate(deepcopy(parentA_nodes)):
        if node in common_nodes:
            offspring_nodes.append(nodes_map[node.id])
        else:
            if len(random_nodes) == 0:
                raise Exception("No more random nodes left")

            new_node = nodes_map[random_nodes.pop(0).id]
            offspring_nodes.append(new_node)

        if ind > 0:
            offspring_nodes[ind - 1].add_next_connection(offspring_nodes[ind])

    offspring_nodes[-1].add_next_connection(offspring_nodes[0])

    return Run(current_id, offspring_nodes, distance_matrix)


def _operator2(
    parents: list[Run], current_id: int, nodes: list[Node], distance_matrix: DistanceMatrix, **kwargs
) -> Run:
    parentA_nodes = parents[0].nodes
    parentB_nodes = parents[1].nodes

    common_nodes = set(parentA_nodes).intersection(set(parentB_nodes))

    if len(common_nodes) == len(parentA_nodes):
        return Run(current_id, deepcopy(parentA_nodes), distance_matrix)

    offspring_nodes = deepcopy(choice(parents).nodes)

    for node in offspring_nodes:
        if node not in common_nodes:
            prev_node, next_node = node.prev_connection, node.next_connection

            node.remove_connection(prev_node).remove_connection(next_node)
            prev_node.add_next_connection(next_node)

    # restore sequence albeit smaller
    offspring_nodes = linked_to_sequence(prev_node)
    # repair sequence to full size
    offspring_nodes = repair(offspring_nodes, set(nodes), distance_matrix, **kwargs)

    return Run(current_id, offspring_nodes, distance_matrix)


def generate_offspring(
    parents: list[Run],
    current_id: int,
    operator: Operator,
    nodes: list[Node],
    distance_matrix: DistanceMatrix,
    **kwargs,
) -> Run:
    if operator == Operator.OPERATOR_1:
        return _operator1(parents, current_id, nodes, distance_matrix, **kwargs)
    elif operator == Operator.OPERATOR_2:
        return _operator2(parents, current_id, nodes, distance_matrix, **kwargs)
    else:
        raise Exception("Invalid operator")


def generate_initial_population(
    initial_runs: list[Run], population_size: int, current_id: int, distance_matrix: DistanceMatrix
) -> tuple[dict[int, Run], int]:
    shuffle(initial_runs)

    population: dict[int, Run] = {}
    population_scores: set[int] = set()

    ind = 0
    while True:
        if len(population) == population_size:
            break

        # possible to generate local search solutions on the fly
        # TODO: allow insufficient unique runs situation by creating new runs
        if len(initial_runs) == ind:
            raise Exception("Unable to create initial population, not enough unique runs")

        if initial_runs[ind].score not in population_scores:
            population_scores.add(initial_runs[ind].score)
            population[current_id] = Run(current_id, deepcopy(initial_runs[ind].nodes), distance_matrix)
            current_id += 1

        ind += 1

    return (population, current_id)
