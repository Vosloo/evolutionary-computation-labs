from src.model import DistanceMatrix, Node
from src.model.delta import Delta
from src.utils import linked_to_sequence

class DeltaIntraEdges(Delta):
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

    def _replace_connections(self, nodeA: Node, nodeB: Node) -> None:
        outerA, outerB = nodeA, nodeB
        innerA, innerB = nodeA.next_connection, nodeB.prev_connection

        outerA.remove_connection(innerA)
        outerB.remove_connection(innerB)

        outerA_ind = None
        innerA_ind = None
        outerB_ind = None
        innerB_ind = None
        
        for ind in range(len(self.original_sequence)):
            curr_node = self.original_sequence[ind]
            if curr_node == outerA:
                outerA_ind = ind
            elif curr_node == innerA:
                innerA_ind = ind
            elif curr_node == outerB:
                outerB_ind = ind
            elif curr_node == innerB:
                innerB_ind = ind
            
            if outerA_ind and innerA_ind and outerB_ind and innerB_ind:
                break

        if innerA_ind < outerA_ind:
            outerA, innerA = innerA, outerA
            outerA_ind, innerA_ind = innerA_ind, outerA_ind
        if outerB_ind < innerB_ind:
            outerB, innerB = innerB, outerB
            outerB_ind, innerB_ind = innerB_ind, outerB_ind

        # TODO: Coś się spierdoliło tutaj

        for node in self.original_sequence[outerA_ind + 1 : outerB_ind]:
            node.reverse_connections()

        outerA.add_next_connection(innerB)
        outerB.add_prev_connection(innerA)
