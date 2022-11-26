from src.model import Node
from src.model.delta import Delta


class DeltaInterNodes(Delta):
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

        for connection in old_node_connections:
            nodeA.remove_connection(connection)

            if connection.prev_connection is None:
                connection.add_prev_connection(nodeB)
            elif connection.next_connection is None:
                connection.add_next_connection(nodeB)
