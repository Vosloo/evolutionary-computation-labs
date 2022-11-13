from enum import Enum, unique


@unique
class Method(Enum):
    RANDOM = "random"
    NEAREST = "nearest"
    GREEDY_CYCLE = "greedy_cycle"
    GREEDY_REGRET = "greedy_regret"
    GREEDY_REGRET_WEIGHTED = "greedy_regret_weighted"
    LOCAL_SEARCH_STEEPEST_NODES_RANDOM = "local_search_steepest_nodes_random"
    LOCAL_SEARCH_STEEPEST_NODES_HEURISTIC = "local_search_steepest_nodes_heuristic"
    LOCAL_SEARCH_STEEPEST_EDGES_RANDOM = "local_search_steepest_edges_random"
    LOCAL_SEARCH_STEEPEST_EDGES_HEURISTIC = "local_search_steepest_edges_heuristic"
    LOCAL_SEARCH_GREEDY_NODES_RANDOM = "local_search_greedy_nodes_random"
    LOCAL_SEARCH_GREEDY_NODES_HEURISTIC = "local_search_greedy_nodes_heuristic"
    LOCAL_SEARCH_GREEDY_EDGES_RANDOM = "local_search_greedy_edges_random"
    LOCAL_SEARCH_GREEDY_EDGES_HEURISTIC = "local_search_greedy_edges_heuristic"
