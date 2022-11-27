from src.model import DistanceMatrix, Node
from src.model.delta import Delta
from src.utils import linked_to_sequence


class DeltaCandidateEdges(Delta):
    def __init__(
        self, nodeA: Node, nodeB: Node, distance_matrix: DistanceMatrix, is_next: bool = True
    ) -> None:
        super().__init__(nodeA, nodeB, distance_matrix)
        self.is_next = is_next

    def apply_nodes(self, original_sequence: list[Node]) -> list[Node]:
        self.original_sequence = original_sequence
        
        nodeA, nodeB = self.nodes
        self._replace_connections(nodeA, nodeB)

        return linked_to_sequence(self.original_sequence[0])


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
        nodeA_ind = None
        nodeB_ind = None
        
        for ind in range(len(self.original_sequence)):
            curr_node = self.original_sequence[ind]
            if curr_node == nodeA:
                nodeA_ind = ind
            elif curr_node == nodeB:
                nodeB_ind = ind
            if nodeA_ind and nodeB_ind:
                break
        
        if nodeA_ind > nodeB_ind:
            nodeA, nodeB = nodeB, nodeA
            nodeA_ind, nodeB_ind = nodeB_ind, nodeA_ind
        
        # node edge connection index
        conn_ind = 1 if self.is_next else 0

        nodeAconn = nodeA.connections[conn_ind]
        nodeBconn = nodeB.connections[conn_ind]

        nodeA.remove_connection(nodeAconn)
        nodeB.remove_connection(nodeBconn)

        for node in self.original_sequence[:nodeA_ind + conn_ind] + self.original_sequence[nodeB_ind + conn_ind:]:
                node.reverse_connections()

        nodeA.add_prev_connection(nodeB)
        nodeAconn.add_prev_connection(nodeBconn)