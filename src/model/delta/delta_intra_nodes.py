from src.model import DistanceMatrix, Node
from src.model.delta import Delta


class DeltaIntraNodes(Delta):
    def apply_nodes(self, original_sequence: list[Node]) -> list[Node]:
        self.original_sequence = original_sequence

        nodeA, nodeB = self.nodes

        nodeA_ind = original_sequence.index(nodeA)
        nodeB_ind = original_sequence.index(nodeB)

        self._replace_connections(nodeA, nodeB)

        original_sequence[nodeA_ind] = nodeB
        original_sequence[nodeB_ind] = nodeA

        return original_sequence

    @property
    def modified_cost(self) -> float:
        return 0

    @property
    def modified_distance(self) -> float:
        return self._delta

    def _get_delta(self, distance_matrix: DistanceMatrix) -> float:
        nodeA, nodeB = self.nodes
        delta = 0

        from_connections = nodeA.connections
        to_connections = nodeB.connections
        for i, from_conn in enumerate(from_connections):
            to_conn = to_connections[i]
            old_dist = distance_matrix.get_distance(
                nodeA, from_conn
            ) + distance_matrix.get_distance(nodeB, to_conn)
            new_dist = distance_matrix.get_distance(nodeA, to_conn) + distance_matrix.get_distance(
                nodeB, from_conn
            )
            delta += new_dist - old_dist  # lower is better

    def _replace_connections(self, nodeA: Node, nodeB: Node) -> None:
        nodeA_connections = nodeA.connections
        nodeB_connections = nodeB.connections            

        for ind, nodeA_conn in enumerate(nodeA_connections):
            nodeB_conn = nodeB_connections[ind]

            nodeA.remove_connection(nodeA_conn)
            nodeB.remove_connection(nodeB_conn)

            if nodeA_conn.prev_connection is None:
                nodeA_conn.add_prev_connection(nodeB)
            elif nodeA_conn.next_connection is None:
                nodeA_conn.add_next_connection(nodeB)

            if nodeB_conn.prev_connection is None:
                nodeB_conn.add_prev_connection(nodeA)
            elif nodeB_conn.next_connection is None:
                nodeB_conn.add_next_connection(nodeA)
