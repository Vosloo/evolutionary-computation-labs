from src.model import DistanceMatrix, Node
from src.model.delta import Delta
from src.utils import linked_to_sequence, find_nodes_in_sequence


class DeltaIntraEdges(Delta):
    def __init__(self, nodeA: Node, nodeB: Node, distance_matrix: DistanceMatrix) -> None:
        super().__init__(nodeA, nodeB, distance_matrix)
        self._applied_to = [nodeA, nodeA.next_connection, nodeB.prev_connection, nodeB]

    def apply_nodes(self, original_sequence: list[Node]) -> list[Node]:
        self.original_sequence = original_sequence

        outerA, outerB = self.nodes
        self._replace_connections(outerA, outerB)

        return linked_to_sequence(self.original_sequence[0])

    @property
    def modified_cost(self) -> float:
        return 0

    @property
    def modified_distance(self) -> float:
        return self.delta

    @property
    def applied_to_nodes(self) -> list[Node]:
        """
        Returns the nodes with the delta applied to them in the order:
        outerA, innerA, innerB, outerB
        """
        return self._applied_to

    def _get_delta(self) -> float:
        """
        Calculates the delta of the edge swap between the two nodes.
        The direction of the swap either from edgeA to edgeB or from edgeB to edgeA
        is not important, as the delta is the same in both cases e.g.:

        Edges: (1, 2) and (6, 7) give the same delta as (6, 7) and (1, 2)
        """
        outerA, outerB = self.nodes
        innerA, innerB = outerA.next_connection, outerB.prev_connection

        # new distace - old distance
        delta = (
            self.distance_matrix.get_distance(outerA, innerB)
            + self.distance_matrix.get_distance(innerA, outerB)
        ) - (
            self.distance_matrix.get_distance(outerA, innerA)
            + self.distance_matrix.get_distance(outerB, innerB)
        )

        return delta

    def _replace_connections(self, nodeA: Node, nodeB: Node) -> None:
        outerA, outerB = nodeA, nodeB
        innerA, innerB = nodeA.next_connection, nodeB.prev_connection

        outerA.remove_connection(innerA)
        outerB.remove_connection(innerB)

        outerA_ind, innerA_ind, outerB_ind, innerB_ind = find_nodes_in_sequence(
            [outerA, innerA, outerB, innerB], self.original_sequence
        )

        # Looping situation in the list
        if innerA_ind < outerA_ind:
            outerA_ind = innerA_ind + 1
        if outerB_ind < innerB_ind:
            outerB_ind = innerB_ind + 1

        # Good placement (A -> B) => OuterA, InnerA then InnerB, OuterB
        if outerA_ind < outerB_ind:
            start_ind = innerA_ind
            end_ind = outerB_ind
            outers_reversed = False

        # Bad placement (B -> A) => InnerB, OuterB then OuterA, InnerA
        else:
            start_ind = innerA_ind
            end_ind = outerB_ind
            outers_reversed = True

        if not outers_reversed:
            for node in self.original_sequence[start_ind:end_ind]:
                node.reverse_connections()
        else:
            for node in self.original_sequence[:end_ind] + self.original_sequence[start_ind:]:
                node.reverse_connections()

        # 1 2 3 4 5 6 7
        # outerA = 5
        # outerB = 2
        # 5 6 7 1 2 3 4

        outerA.add_next_connection(innerB)
        outerB.add_prev_connection(innerA)

        pass
