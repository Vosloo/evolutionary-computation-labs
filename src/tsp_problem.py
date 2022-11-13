from copy import deepcopy
from time import perf_counter

from src.algorithms.greedy_cycle import greedy_cycle
from src.algorithms.greedy_regret import greedy_regret
from src.algorithms.methods import Method
from src.algorithms.nearest_neighbour import nearest
from src.algorithms.random import random
from src.data_loader import DataLoader
from src.model import DistanceMatrix, Grade, Instance, Node, Run

TYPE_METHOD_GRADES = dict[str, Grade]
TYPE_INSTANCE_GRADES = dict[str, TYPE_METHOD_GRADES]

params = {
    Method.RANDOM: {},
    Method.NEAREST: {},
    Method.GREEDY_CYCLE: {},
    Method.GREEDY_REGRET: {
        "k_regret": 2,
    },
    Method.GREEDY_REGRET_WEIGHTED: {
        "k_regret": 2,
        "regret_weights": [0.5, 0.5],
    },
}


class TSPProblem:
    def __init__(self, no_runs: int = 200) -> None:
        self.instances = DataLoader.load_tsp_instances()

        self.no_runs = no_runs
        self.methods = {
            Method.RANDOM: random,
            Method.NEAREST: nearest,
            Method.GREEDY_CYCLE: greedy_cycle,
            Method.GREEDY_REGRET: greedy_regret,
            Method.GREEDY_REGRET_WEIGHTED: greedy_regret,
        }
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
            grades = self._grade_methods(nodes, distance_matrix, methods)
            instance_grades[instance_name] = grades

        return instance_grades

    def _get_nodes(self, instance: Instance) -> list[Node]:
        return [
            Node(i, x, y, cost)
            for i, (x, y, cost) in enumerate(zip(instance.x, instance.y, instance.cost))
        ]

    def _grade_method(
        self, nodes: list[Node], method_name: Method, method: callable, distance_matrix: DistanceMatrix
    ) -> Grade:
        runs: list[Run] = []
        best_run: Run = None

        for pivot_ind in range(self.no_runs):
            print(f"\r{pivot_ind + 1:3} / {self.no_runs:3}", end="")
            nodes_cp = deepcopy(nodes)
            pivot_node = nodes_cp[pivot_ind]

            parameters = {
                "pivot_node": pivot_node,
                "nodes": nodes_cp,
                "node_coverage": round(len(nodes_cp) / 2),
                "distance_matrix": distance_matrix,
            } | params[method_name]

            selected_nodes = method(**parameters)

            curr_run = Run(pivot_ind, selected_nodes, distance_matrix)
            runs.append(curr_run)

            if best_run is None or curr_run < best_run:
                best_run = curr_run

        meth_name = method_name.value.replace("_", " ").title()
        return Grade(meth_name, best_run, runs)

    def _grade_methods(
        self, nodes: list[Node], distance_matrix: DistanceMatrix, methods: list[Method] = None
    ) -> TYPE_METHOD_GRADES:
        grades: TYPE_METHOD_GRADES = {}

        if methods is None:
            selected_methods = self.methods
        else:
            selected_methods = {method: self.methods[method] for method in methods}

        for method_name, method in selected_methods.items():
            print(f"Running {method_name.name} method for {self.no_runs} runs")
            start = perf_counter()
            grade = self._grade_method(nodes, method_name, method, distance_matrix)
            print(f"\rFinished {method_name.name} method in {perf_counter() - start:.2f}s")
            grades[method_name] = grade

        return grades
