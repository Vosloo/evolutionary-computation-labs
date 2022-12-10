from copy import deepcopy
from time import perf_counter

from src.algorithms import (
    Method,
    greedy_cycle,
    greedy_regret,
    local_search,
    local_search_candidates,
    local_search_iterative,
    local_search_moves,
    local_search_MSLS,
    local_search_LSN,
    nearest,
    random_sequence,
)
from src.data_loader import DataLoader
from src.model import DistanceMatrix, Grade, Instance, Node, Run

TYPE_METHOD_GRADES = dict[str, Grade]
TYPE_INSTANCE_GRADES = dict[str, TYPE_METHOD_GRADES]

params = {
    Method.RANDOM_SEQUENCE: {},
    Method.NEAREST: {},
    Method.GREEDY_CYCLE: {},
    Method.GREEDY_REGRET: {
        "k_regret": 2,
    },
    Method.GREEDY_REGRET_WEIGHTED: {
        "k_regret": 2,
        "regret_weights": [0.5, 0.5],
    },
    Method.LOCAL_SEARCH_STEEPEST_NODES_RANDOM: {
        "search_type": "steepest",
        "intra_type": "nodes",
        "use_heuristic": False,
    },
    Method.LOCAL_SEARCH_STEEPEST_NODES_HEURISTIC: {
        "search_type": "steepest",
        "intra_type": "nodes",
        "use_heuristic": True,
    },
    Method.LOCAL_SEARCH_STEEPEST_EDGES_RANDOM: {
        "search_type": "steepest",
        "intra_type": "edges",
        "use_heuristic": False,
    },
    Method.LOCAL_SEARCH_STEEPEST_EDGES_HEURISTIC: {
        "search_type": "steepest",
        "intra_type": "edges",
        "use_heuristic": True,
    },
    Method.LOCAL_SEARCH_GREEDY_NODES_RANDOM: {
        "search_type": "greedy",
        "intra_type": "nodes",
        "use_heuristic": False,
    },
    Method.LOCAL_SEARCH_GREEDY_NODES_HEURISTIC: {
        "search_type": "greedy",
        "intra_type": "nodes",
        "use_heuristic": True,
    },
    Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM: {
        "search_type": "greedy",
        "intra_type": "edges",
        "use_heuristic": False,
    },
    Method.LOCAL_SEARCH_GREEDY_EDGES_HEURISTIC: {
        "search_type": "greedy",
        "intra_type": "edges",
        "use_heuristic": True,
    },
    Method.LOCAL_SEARCH_CANDIDATES_RANDOM: {
        "no_candidates": 10,
        "use_heuristic": False,
    },
    Method.LOCAL_SEARCH_CANDIDATES_HEURISTIC: {
        "no_candidates": 10,
        "use_heuristic": True,
    },
    Method.LOCAL_SEARCH_MOVES_RANDOM: {
        "use_heuristic": False,
    },
    Method.LOCAL_SEARCH_MSLS: {
        "no_iterations": 200,
    },
    Method.LOCAL_SEARCH_ITERATIVE: {
        "max_runtime": 105,
    },
    Method.LOCAL_SEARCH_LSN_NO_LS: {
        "max_runtime": 105,
        "is_local_search_enabled": False,
        "k_regret": 2,
        "regret_weights": [0.5, 0.5],
    },
    Method.LOCAL_SEARCH_LSN_WITH_LS: {
        "max_runtime": 105,
        "is_local_search_enabled": True,
        "k_regret": 2,
        "regret_weights": [0.5, 0.5],
    },
}


class TSPProblem:
    def __init__(self, no_runs: int = 200) -> None:
        self.instances = DataLoader.load_tsp_instances()

        self.no_runs = no_runs
        self.methods = {
            Method.RANDOM_SEQUENCE: random_sequence,
            Method.NEAREST: nearest,
            Method.GREEDY_CYCLE: greedy_cycle,
            Method.GREEDY_REGRET: greedy_regret,
            Method.GREEDY_REGRET_WEIGHTED: greedy_regret,
            Method.LOCAL_SEARCH_STEEPEST_NODES_RANDOM: local_search,
            Method.LOCAL_SEARCH_STEEPEST_NODES_HEURISTIC: local_search,
            Method.LOCAL_SEARCH_STEEPEST_EDGES_RANDOM: local_search,
            Method.LOCAL_SEARCH_STEEPEST_EDGES_HEURISTIC: local_search,
            Method.LOCAL_SEARCH_GREEDY_NODES_RANDOM: local_search,
            Method.LOCAL_SEARCH_GREEDY_NODES_HEURISTIC: local_search,
            Method.LOCAL_SEARCH_GREEDY_EDGES_RANDOM: local_search,
            Method.LOCAL_SEARCH_GREEDY_EDGES_HEURISTIC: local_search,
            Method.LOCAL_SEARCH_CANDIDATES_RANDOM: local_search_candidates,
            Method.LOCAL_SEARCH_CANDIDATES_HEURISTIC: local_search_candidates,
            Method.LOCAL_SEARCH_MOVES_RANDOM: local_search_moves,
            Method.LOCAL_SEARCH_MSLS: local_search_MSLS,
            Method.LOCAL_SEARCH_ITERATIVE: local_search_iterative,
            Method.LOCAL_SEARCH_LSN_NO_LS: local_search_LSN,
            Method.LOCAL_SEARCH_LSN_WITH_LS: local_search_LSN,
        }
        self.heuristic_grade = {}
        self.random_grade = {}
        print(f"Available methods: {[method.name for method in self.methods.keys()]}")

    def run(self, instances: list[str] = None, methods: list[Method] = None) -> TYPE_INSTANCE_GRADES:
        instance_grades = {}

        if instances is None:
            selected_instances = self.instances
        else:
            selected_instances = {instance: self.instances[instance] for instance in instances}

        for instance_name, instance in selected_instances.items():
            print(f"\nRunning {instance_name} instance")
            distance_matrix = DistanceMatrix(instance)
            nodes = self._get_nodes(instance)
            grades = self._grade_methods(instance_name, nodes, distance_matrix, methods)
            instance_grades[instance_name] = grades

        return instance_grades

    def _get_nodes(self, instance: Instance) -> list[Node]:
        """
        Returns list of nodes from instance creating connections between them.
        """
        nodes: list[Node] = []
        for i, (x, y, cost) in enumerate(zip(instance.x, instance.y, instance.cost)):
            curr_node = Node(i, x, y, cost)
            nodes.append(curr_node)

        return nodes

    def _grade_method(
        self,
        instance_name: str,
        nodes: list[Node],
        method_name: Method,
        method: callable,
        distance_matrix: DistanceMatrix,
    ) -> Grade:
        runs: list[Run] = []
        best_run: Run = None

        for pivot_ind in range(self.no_runs):
            print(f"\r{pivot_ind + 1:3} / {self.no_runs:3}", end="")
            nodes_cp = deepcopy(nodes)
            pivot_node = nodes_cp[pivot_ind]

            if (
                params[method_name].get("use_heuristic", False)
                and self.heuristic_grade.get(instance_name) is not None
            ):
                initial_solution = deepcopy(self.heuristic_grade[instance_name].best_run.nodes)
            elif self.random_grade.get(instance_name) is not None:
                initial_solution = deepcopy(self.random_grade[instance_name].best_run.nodes)
            else:
                initial_solution = None

            parameters = {
                "pivot_node": pivot_node,
                "nodes": nodes_cp,
                "node_coverage": round(len(nodes_cp) / 2),
                "distance_matrix": distance_matrix,
                "initial_solution": initial_solution,
            } | params[method_name]

            selected_nodes = method(**parameters)
            first_node = selected_nodes[0]

            curr_run = Run(first_node.id, selected_nodes, distance_matrix)
            runs.append(curr_run)

            if best_run is None or curr_run < best_run:
                best_run = curr_run

        meth_name = method_name.value.replace("_", " ").title()
        return Grade(meth_name, best_run, runs)

    def _grade_methods(
        self,
        instance_name: str,
        nodes: list[Node],
        distance_matrix: DistanceMatrix,
        methods: list[Method] = None,
    ) -> TYPE_METHOD_GRADES:
        grades: TYPE_METHOD_GRADES = {}

        if methods is None:
            selected_methods = self.methods
        else:
            selected_methods = {method: self.methods[method] for method in methods}

        for method_name, method in selected_methods.items():
            print(f"Running {method_name.name} method for {self.no_runs} runs")
            start = perf_counter()
            grade = self._grade_method(instance_name, nodes, method_name, method, distance_matrix)
            if method_name == Method.GREEDY_REGRET_WEIGHTED:
                self.heuristic_grade[instance_name] = grade
            elif method_name == Method.RANDOM_SEQUENCE:
                self.random_grade[instance_name] = grade

            end = perf_counter()
            grade.set_runtime(end - start)
            print(f"\rFinished {method_name.name} method in {end - start:.2f}s")
            grades[method_name] = grade

        return grades
