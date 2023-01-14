from enum import Enum, unique


@unique
class Method(Enum):
    RANDOM_SEQUENCE = "random_sequence"
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
    LOCAL_SEARCH_CANDIDATES_RANDOM = "local_search_candidates_random"
    LOCAL_SEARCH_CANDIDATES_HEURISTIC = "local_search_candidates_heuristic"
    LOCAL_SEARCH_MOVES_RANDOM = "local_search_moves_random"
    LOCAL_SEARCH_MSLS = "local_search_msls"
    LOCAL_SEARCH_ITERATIVE = "local_search_iterative"
    LOCAL_SEARCH_LSN_NO_LS = "local_search_lsn_no_ls"
    LOCAL_SEARCH_LSN_WITH_LS = "local_search_lsn_with_ls"
    HYBRID_EVOLUTION_OPERATOR_1 = "hybrid_evolution_operator_1"
    HYBRID_EVOLUTION_OPERATOR_1_NO_LS = "hybrid_evolution_operator_1_no_ls"
    HYBRID_EVOLUTION_OPERATOR_2 = "hybrid_evolution_operator_2"
    HYBRID_EVOLUTION_OPERATOR_2_NO_LS = "hybrid_evolution_operator_2_no_ls"
