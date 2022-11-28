from src.model import Node, DistanceMatrix
from src.model.delta import Delta


class DeltaInterNodes(Delta):
    def __init__(self, nodeA: Node, nodeB: Node, distance_matrix: DistanceMatrix) -> None:
        super().__init__(nodeA, nodeB, distance_matrix)
        self._applied_to: list[Node] = [
            nodeA.prev_connection,
            nodeA,
            nodeA.next_connection,
            nodeB.prev_connection,
            nodeB,
            nodeB.next_connection,
        ]

    def apply_nodes(self, original_sequence: list[Node]) -> list[Node]:
        self.original_sequence = original_sequence

        old_node, new_node = self.nodes

        self._replace_connections(old_node, new_node)

        old_ind = original_sequence.index(old_node)
        original_sequence[old_ind] = new_node

        return original_sequence

    @property
    def modified_cost(self) -> float:
        old_node, new_node = self.nodes
        return new_node.cost - old_node.cost

    @property
    def modified_distance(self) -> float:
        return self.delta - self.modified_cost

    @property
    def applied_to_nodes(self) -> list[Node]:
        """
        Returns the nodes with the delta applied to them in the order:

        nodeA_prev, nodeA, innerA, innerB, nodeB, nodeB_next
        """
        return self._applied_to

    def _get_delta(self) -> float:
        old_node, new_node = self.nodes
        delta = 0

        connections = old_node.connections
        for conn in connections:
            if old_node is None or new_node is None or conn is None:
                pass

            old_dist = self.distance_matrix.get_distance(old_node, conn)
            new_dist = self.distance_matrix.get_distance(new_node, conn)
            delta += new_dist - old_dist  # lower is better

        delta += new_node.cost - old_node.cost  # lower is better

        return delta

    def _replace_connections(self, nodeA: Node, nodeB: Node) -> None:
        old_node_connections = nodeA.connections
        if old_node_connections == [None, None]:
            raise ValueError("Node has no connections!")

        for connection in old_node_connections:
            nodeA.remove_connection(connection)

            if connection.prev_connection is None:
                connection.add_prev_connection(nodeB)
            elif connection.next_connection is None:
                connection.add_next_connection(nodeB)
