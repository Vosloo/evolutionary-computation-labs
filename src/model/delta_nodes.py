from __future__ import annotations

from src.model import DistanceMatrix, Node


class DeltaNodes:
    def __init__(
        self, node1: Node, node2: Node, is_outer: bool, distance_matrix: DistanceMatrix
    ) -> None:
        self.nodes = (node1, node2)
        self.is_outer = is_outer
        self.delta = self._get_delta(distance_matrix)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, DeltaNodes):
            return self.delta == o.delta

        return False

    def __lt__(self, o: DeltaNodes) -> bool:
        return self.delta < o.delta

    def _get_delta(self, distance_matrix: DistanceMatrix) -> float:
        from_node, to_node = self.nodes
        delta = 0

        # 1 2 3 4 5 6
        # (2, 8)
        # 1 8 3 4 5 6
        if self.is_outer:
            connections = from_node.connections
            for conn in connections:
                old_dist = distance_matrix.get_nodes_distance(from_node, conn)
                new_dist = distance_matrix.get_nodes_distance(to_node, conn)
                delta += new_dist - old_dist  # lower is better

            delta += to_node.cost - from_node.cost  # lower is better

        # 1 2 3 4 5 6
        # (2, 5)
        # 1 5 3 4 2 6
        else:
            from_connections = from_node.connections
            to_connections = to_node.connections
            for i, from_conn in enumerate(from_connections):
                to_conn = to_connections[i]
                old_dist = distance_matrix.get_nodes_distance(
                    from_node, from_conn
                ) + distance_matrix.get_nodes_distance(to_node, to_conn)
                new_dist = distance_matrix.get_nodes_distance(
                    from_node, to_conn
                ) + distance_matrix.get_nodes_distance(to_node, from_conn)
                delta += new_dist - old_dist  # lower is better

        return delta
