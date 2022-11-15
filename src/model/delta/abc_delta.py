from __future__ import annotations

from abc import ABC, abstractmethod

from src.model import DistanceMatrix, Node


class ADelta(ABC):
    def __init__(self, nodeA: Node, nodeB: Node, distance_matrix: DistanceMatrix) -> None:
        self.nodes = (nodeA, nodeB)
        self.delta = self._delta(distance_matrix)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, ADelta):
            return self.delta == o.delta

        return False

    def __lt__(self, o: ADelta) -> bool:
        return self.delta < o.delta

    @abstractmethod
    def _get_delta(self, distance_matrix: DistanceMatrix) -> float:
        ...
