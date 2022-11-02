from copy import deepcopy
from time import perf_counter

from src.algorithms.nearest_neighbour import nearest
from src.data_loader import DataLoader
from src.model import DistanceMatrix, Grade, Instance, Node, Run

TYPE_METHOD_GRADES = dict[str, Grade]
TYPE_INSTANCE_GRADES = dict[str, TYPE_METHOD_GRADES]

params = {
    "k_regret": 2,
    "regret_weights": [0.5, 0.5],
}


class TSPProblem:
    def __init__(self, no_runs: int = 200) -> None:
        self.instances = DataLoader.load_tsp_instances()

        self.no_runs = no_runs
        self.methods = {
            nearest.__name__: nearest,
        }

    def run(self) -> TYPE_INSTANCE_GRADES:
        instance_grades = {}
        for instance_name, instance in self.instances.items():
            print(f"\nRunning {instance_name} instance")
            distance_matrix = DistanceMatrix(instance)
            nodes = self._get_nodes(instance)
            grades = self._grade_methods(nodes, distance_matrix)
            instance_grades[instance_name] = grades

        return instance_grades

    def _get_nodes(self, instance: Instance) -> list[Node]:
        return [
            Node(i, x, y, cost)
            for i, (x, y, cost) in enumerate(zip(instance.x, instance.y, instance.cost))
        ]

    def _grade_method(
        self, nodes: list[Node], method: callable, distance_matrix: DistanceMatrix
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
            } | params

            selected_nodes = method(**parameters)

            curr_run = Run(pivot_ind, selected_nodes, distance_matrix)
            runs.append(curr_run)

            if best_run is None or curr_run < best_run:
                best_run = curr_run

        return Grade(method.__name__, best_run, runs)

    def _grade_methods(self, nodes: list[Node], distance_matrix: DistanceMatrix) -> TYPE_METHOD_GRADES:
        grades: TYPE_METHOD_GRADES = {}
        for method_name, method in self.methods.items():
            print(f"Running {method_name} method for {self.no_runs} runs")
            start = perf_counter()
            grade = self._grade_method(nodes, method, distance_matrix)
            print(f"\rFinished {method_name} method in {perf_counter() - start:.2f}s")
            grades[method_name] = grade

        return grades
