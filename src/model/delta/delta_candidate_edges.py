from src.model import DistanceMatrix, Node
from src.model.delta import Delta


class DeltaCandidateEdges(Delta):
    def __init__(
        self, nodeA: Node, nodeB: Node, distance_matrix: DistanceMatrix, is_next: bool = True
    ) -> None:
        super().__init__(nodeA, nodeB, distance_matrix)
        self.is_next = is_next

    def apply_nodes(self, original_sequence: list[Node]) -> list[Node]:
        ...

    @property
    def modified_cost(self) -> float:
        return 0

    @property
    def modified_distance(self) -> float:
        return self.delta

    def _get_delta(self) -> float:
        nodeA, nodeB = self.nodes
        
        if self.is_next:
            nodeAconn = nodeA.next_connection
            nodeBconn = nodeB.next_connection
        else:
            nodeAconn = nodeA.prev_connection
            nodeBconn = nodeB.prev_connection

        delta = (
            self.distance_matrix.get_distance(nodeA, nodeB)
            + self.distance_matrix.get_distance(nodeAconn, nodeBconn)
            - (
                self.distance_matrix.get_distance(nodeA, nodeAconn)
                + self.distance_matrix.get_distance(nodeB, nodeBconn)
            )
        )

        return delta

    def _replace_connections(self, nodeA: Node, nodeB: Node) -> None:
        if self.is_next:
            outerA, outerB = nodeA, nodeB.next_connection
            innerA, innerB = nodeA.next_connection, nodeB
        else:
            outerA, outerB = nodeA.prev_connection, nodeB
            innerA, innerB = nodeA, nodeB.prev_connection

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

        # Pseudo-code:
        if outerA_ind < innerA_ind:
            if innerA_ind < outerA_ind:
                outerA_ind = innerA_ind + 1
            if outerB_ind < innerB_ind:
                outerB_ind = innerB_ind + 1
        # else:
        #     if innerA_ind < outerA_ind:
        #         outerA_ind = innerA_ind - 1
        #     if outerB_ind < innerB_ind:
        #         outerB_ind = innerB_ind - 1

        # 1 2 3 4 5 6

        # (3, 4), (6, 1) 

        # outerA - 3
        # outerB - 1

        # outerA_ind - 0
        # outerB_ind - 4

        # 1 2 3 4 5 6
        # 1 2 3 6 5 4
        
        for node in self.original_sequence[outerA_ind + 1 : outerB_ind]:
            node.reverse_connections()

        outerA.add_next_connection(innerB)
        outerB.add_prev_connection(innerA)
