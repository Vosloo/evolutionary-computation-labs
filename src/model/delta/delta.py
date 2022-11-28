from __future__ import annotations

from abc import ABC, abstractmethod

from src.model import DistanceMatrix, Node


class Delta(ABC):
    def __init__(self, nodeA: Node, nodeB: Node, distance_matrix: DistanceMatrix) -> None:
        self.nodes = (nodeA, nodeB)
        self.distance_matrix: DistanceMatrix = distance_matrix
        self._delta: float = None
        self.original_sequence: list[Node] | None = None

        self._applied_to: list[Node] | None = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Delta):
            return self.delta == other.delta

        return False

    def __lt__(self, other: Delta) -> bool:
        if isinstance(other, Delta):
            return self.delta < other.delta

        return self.delta < other

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

    @property
    def delta(self) -> float:
        if self._delta is None:
            self._delta = self._get_delta()

        return self._delta

    @property
    def applied_to_nodes(self) -> list[Node] | None:
        """
        Returns the nodes with the delta applied to them in the order:
        outerA, innerA, innerB, outerB
        """
        return self._applied_to

    @abstractmethod
    def _get_delta(self) -> float:
        ...

    @abstractmethod
    def _replace_connections(self, nodeA: Node, nodeB: Node) -> None:
        ...
