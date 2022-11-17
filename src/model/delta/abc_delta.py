from __future__ import annotations

from abc import ABC, abstractmethod

from src.model import DistanceMatrix, Node


class ADelta(ABC):
    def __init__(self, nodeA: Node, nodeB: Node, distance_matrix: DistanceMatrix) -> None:
        self.nodes = (nodeA, nodeB)
        self._delta: float = self._get_delta(distance_matrix)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ADelta):
            return self._delta == other._delta

        return False

    def __lt__(self, other: ADelta) -> bool:
        if isinstance(other, ADelta):
            return self._delta < other._delta
        
        return self._delta < other

    @abstractmethod
    def apply_nodes(self, original_sequence: list[Node]) -> None:
        """
        Applies (replaces) the delta nodes to the original sequence.
        """
        ...

    @property
    @abstractmethod
    def modified_cost(self) -> float:
        ...

    @property
    @abstractmethod
    def modified_distance(self) -> float:
        ...

    @abstractmethod
    def _get_delta(self, distance_matrix: DistanceMatrix) -> float:
        ...