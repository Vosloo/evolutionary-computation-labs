from src.model import DistanceMatrix, Node
from src.model.delta import ADelta


class DeltaInterNodes(ADelta):
    def apply_nodes(self, original_sequence: list[Node]) -> list[Node]:
        from_node, to_node = self.nodes

        to_node.set_connections(from_node.connections)
        from_ind = original_sequence.index(from_node)
        original_sequence[from_ind] = to_node

        return original_sequence

    @property
    def modified_cost(self) -> float:
        from_node, to_node = self.nodes
        return to_node.cost - from_node.cost

    @property
    def modified_distance(self) -> float:
        return self._delta - self.modified_cost

    def _get_delta(self, distance_matrix: DistanceMatrix) -> float:
        from_node, to_node = self.nodes
        delta = 0

        connections = from_node.connections
        for conn in connections:
            old_dist = distance_matrix.get_distance(from_node, conn)
            new_dist = distance_matrix.get_distance(to_node, conn)
            delta += new_dist - old_dist  # lower is better

        delta += to_node.cost - from_node.cost  # lower is better

        return delta
