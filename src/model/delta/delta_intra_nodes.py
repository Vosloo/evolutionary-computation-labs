from src.model import DistanceMatrix, Node
from src.model.delta import ADelta


class DeltaIntraNodes(ADelta):
    def apply_nodes(self, original_sequence: list[Node]) -> list[Node]:
        from_node, to_node = self.nodes

        from_ind = original_sequence.index(from_node)
        to_ind = original_sequence.index(to_node)

        from_connections = from_node.connections
        from_node.set_connections(to_node.connections)
        to_node.set_connections(from_connections)

        original_sequence[from_ind] = to_node
        original_sequence[to_ind] = from_node

        return original_sequence

    @property
    def modified_cost(self) -> float:
        return 0

    @property
    def modified_distance(self) -> float:
        return self._delta

    def _get_delta(self, distance_matrix: DistanceMatrix) -> float:
        from_node, to_node = self.nodes
        delta = 0

        from_connections = from_node.connections
        to_connections = to_node.connections
        for i, from_conn in enumerate(from_connections):
            to_conn = to_connections[i]
            old_dist = distance_matrix.get_distance(
                from_node, from_conn
            ) + distance_matrix.get_distance(to_node, to_conn)
            new_dist = distance_matrix.get_distance(from_node, to_conn) + distance_matrix.get_distance(
                to_node, from_conn
            )
            delta += new_dist - old_dist  # lower is better
