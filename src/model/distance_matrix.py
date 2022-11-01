import numpy as np
from src.model import Instance, Node


class DistanceMatrix:
    def __init__(self) -> None:
        self.distance_matrix: np.array | None = None

    def calculate_distance_matrix(self, instance: Instance) -> None:
        """Calculate the distance matrix for the given instance.

        Args:
            instance (Instance): Instance for which the distance matrix should be calculated.
        """
        if self.distance_matrix is not None:
            return

        coordinates = instance.get_coordinates()

        p1 = np.sum(coordinates**2, axis=1)[:, np.newaxis]
        p2 = np.sum(coordinates**2, axis=1)
        p3 = -2 * np.dot(coordinates, coordinates.T)

        self.distance_matrix = np.array(np.sqrt(p1 + p2 + p3)).astype(int)

    def get_nearest_node(self, pivot_node: Node, other_nodes: list[Node]) -> Node:
        """Get the nearest node to the pivot node from the list of other nodes.

        Args:
            pivot_node (Node): The pivot node.
            other_nodes (list[Node]): The list of other nodes.

        Returns:
            Node: The nearest node to the pivot node.
        """
        assert self.distance_matrix is not None, "Distance matrix is not initialized!"

        min_distance = float("inf")
        min_node = None
        for node in other_nodes:
            if node == pivot_node:
                continue

            distance = self.distance_matrix[pivot_node.id, node.id] + node.cost

            if distance < min_distance:
                min_distance = distance
                min_node = node

        return min_node
