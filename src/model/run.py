from __future__ import annotations

from dataclasses import dataclass

from src.model import Delta, DistanceMatrix, Node


@dataclass
class Run:
    def __init__(self, id: int, selected_nodes: list[Node], distance_matrix: DistanceMatrix) -> None:
        self.id: int = id
        self._selected_nodes: list[Node] = selected_nodes

        for ind, node in enumerate(selected_nodes[:-1]):
            if node.next_connection != selected_nodes[ind + 1]:
                raise ValueError(f"Selected nodes {node} are not connected")
        if selected_nodes[0].prev_connection != selected_nodes[-1]:
            raise ValueError(f"Selected nodes {selected_nodes[0]} are not connected") 

        self._distance_matrix: DistanceMatrix = distance_matrix

        self.cost: int = self._calculate_cost()
        self.distance: int = self._calculate_distance()

    def __repr__(self) -> str:
        return f"Run(id={self.id}, cost={self.cost}, distance={self.distance})"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Run):
            return False

        return self.score == __o.score

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Run):
            return False

        return self.score > other.score

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Run):
            return False

        return self.score < other.score

    @property
    def nodes(self) -> list[Node]:
        return self._selected_nodes

    @property
    def score(self) -> int:
        return self.cost + self.distance

    @staticmethod
    def from_delta(current_run: Run, delta: Delta) -> Run:
        modified_nodes = delta.apply_nodes(current_run.nodes)

        node_id = current_run.nodes[0].id
        mod_cost = delta.modified_cost
        mod_dist = delta.modified_distance

        return current_run._modify_run(node_id, mod_cost, mod_dist, modified_nodes)

    def _modify_run(self, id: int, mod_cost: int, mod_dist: int, modified_nodes: list[Node]) -> Run:
        self.id = id
        self.cost += mod_cost
        self.distance += mod_dist
        self._selected_nodes = modified_nodes

        return self

    def _calculate_cost(self) -> int:
        return sum(node.cost for node in self._selected_nodes)

    def _calculate_distance(self) -> int:
        return sum(
            self._distance_matrix.get_distance(node, self._selected_nodes[i + 1])
            for i, node in enumerate(self._selected_nodes[:-1])
        ) + self._distance_matrix.get_distance(self._selected_nodes[0], self._selected_nodes[-1])
