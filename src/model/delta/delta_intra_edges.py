from src.model import DistanceMatrix, Node
from src.model.delta import ADelta


class DeltaIntraEdges(ADelta):
    def apply_nodes(self, original_sequence: list[Node]) -> list[Node]:
        outerA, outerB = self.nodes
        innerA, innerB = outerA.connections[1], outerB.connections[0]

        outerA.remove_connection(innerA)
        outerB.remove_connection(innerB)

        outerA.add_connection(innerB)
        outerB.add_connection(innerA)

        A_ind = original_sequence.index(outerA)
        B_ind = original_sequence.index(outerB)

        original_sequence[A_ind + 1 : B_ind] = original_sequence[B_ind - 1 : A_ind : -1]

        return original_sequence

    @property
    def modified_cost(self) -> float:
        return 0

    @property
    def modified_distance(self) -> float:
        return self._delta

    def _get_delta(self, distance_matrix: DistanceMatrix) -> float:
        """
        Calculates the delta of the edge swap between the two nodes.
        The direction of the swap either from edgeA to edgeB or from edgeB to edgeA
        is not important, as the delta is the same in both cases e.g.:

        Edges: (1, 2) and (6, 7) give the same delta as (6, 7) and (1, 2)
        """
        outerA, outerB = self.nodes

        edgeA, edgeB = (outerA, outerA.connections[1]), (outerB.connections[0], outerB)

        # new distace - old distance
        delta = (
            distance_matrix.get_distance(edgeA[0], edgeB[0])
            + distance_matrix.get_distance(edgeA[1], edgeB[1])
        ) - (distance_matrix.get_distance(*edgeA) + distance_matrix.get_distance(*edgeB))

        return delta
