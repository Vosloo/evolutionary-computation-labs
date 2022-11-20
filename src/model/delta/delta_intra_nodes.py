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
        return self.delta

    def _get_delta(self) -> float:
        nodeA, nodeB = self.nodes
        delta = 0

        nodeA_connections = nodeA.connections
        nodeB_connections = nodeB.connections
        

        for nodeA_conn, nodeB_conn in zip(nodeA_connections, nodeB_connections):
            old_dist = self.distance_matrix.get_distance(
                nodeA, nodeA_conn
            ) + self.distance_matrix.get_distance(nodeB, nodeB_conn)

            if nodeA_conn != nodeB:
                distA = self.distance_matrix.get_distance(nodeA_conn, nodeB)
            else:
                distA = self.distance_matrix.get_distance(nodeA, nodeB)

            if nodeB_conn != nodeA:
                distB = self.distance_matrix.get_distance(nodeB_conn, nodeA)
            else:
                distB = self.distance_matrix.get_distance(nodeB, nodeA)
            
            new_dist = distA + distB

            delta += new_dist - old_dist  # lower is better

        return delta

    def _replace_connections(self, nodeA: Node, nodeB: Node) -> None:
        if nodeB in nodeA.connections:
            ind = nodeA.connections.index(nodeB)
            
            nodeA_connections = nodeA.connections
            nodeB_connections = nodeB.connections

            nodeA.remove_connection(nodeA_connections[1 - ind])
            nodeB.remove_connection(nodeB_connections[ind]) 
            
            nodeA.reverse_connections()
            nodeB.reverse_connections()
            
            if ind == 0:
                # Case when nodeA and nodeB are first and last nodes in the sequence
                nodeA.add_prev_connection(nodeB_connections[ind])
                nodeB.add_next_connection(nodeA_connections[1 - ind])
            else:
                nodeA.add_next_connection(nodeB_connections[ind])
                nodeB.add_prev_connection(nodeA_connections[1 - ind])

            return

        for nodeA_conn, nodeB_conn in zip(nodeA.connections, nodeB.connections):
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
