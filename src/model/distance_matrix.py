import numpy as np
from src.model import Instance, Node


class DistanceMatrix:
    def __init__(self, instance: Instance) -> None:
        self.instance = instance
        self.distance_matrix: np.ndarray = self._calculate_distance_matrix(instance)

    def _calculate_distance_matrix(self, instance: Instance) -> np.ndarray:
        """Calculate the distance matrix for the given instance.

        Args:
            instance (Instance): Instance for which the distance matrix should be calculated.
        
        Returns:
            np.ndarray: The distance matrix.
        """
        coordinates = instance.get_coordinates()

        p1 = np.sum(coordinates**2, axis=1)[:, np.newaxis]
        p2 = np.sum(coordinates**2, axis=1)
        p3 = -2 * np.dot(coordinates, coordinates.T)

        return np.round(np.array(np.sqrt(p1 + p2 + p3))).astype(int)

    def get_nearest_node(self, pivot_node: Node, other_nodes: list[Node]) -> Node:
        """Get the nearest node to the pivot node from the list of other nodes.

        Args:
            pivot_node (Node): The pivot node.
            other_nodes (list[Node]): The list of other nodes.

        Returns:
            Node: The nearest node to the pivot node.
        """
        min_distance = float("inf")
        min_node = None
        for node in other_nodes:
            distance = self.distance_matrix[pivot_node.id, node.id] + node.cost
            # print(f"Distance from {pivot_node} to {node} is {distance}")
            if distance < min_distance:
                min_distance = distance
                min_node = node

        return min_node

    def get_distance(self, node: Node, other_node: Node) -> int:
        res = self.distance_matrix[node.id][other_node.id]
        return res

    def get_node_to_edge_distance(self, node: Node, edge: tuple[Node, Node], include_cost: bool = True) -> int:
        anchor_1, anchor_2 = edge

        distance = (
            self.distance_matrix[anchor_1.id][node.id]
            + self.distance_matrix[anchor_2.id][node.id]
            - self.distance_matrix[anchor_1.id][anchor_2.id]
        )

        if include_cost:
            distance += node.cost

        return distance
