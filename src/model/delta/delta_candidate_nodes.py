from src.model import DistanceMatrix, Node
from src.model.delta import Delta


class DeltaCandidateNodes(Delta):
    def apply_nodes(self, original_sequence: list[Node]) -> list[Node]:
        ...

    @property
    def modified_cost(self) -> float:
        ...

    @property
    def modified_distance(self) -> float:
        ...

    def _get_delta(self) -> float:
        ...

    def _replace_connections(self, nodeA: Node, nodeB: Node) -> None:
        ...
