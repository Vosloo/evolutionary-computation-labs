from __future__ import annotations


class Node:
    def __init__(self, id, x, y, cost) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.cost = cost
        self.connections: list[Node] = []

    def add_connection(self, node: Node, to_left: bool = False) -> None:
        """
        Adds a node to the connections of current node and vice versa.
        
        :param node: Node to add
        :param to_left: If true, the node will be added to the left of the current node 
        (Careful: the current node will be added to the right of the node anyway!)
        """
        if to_left:
            self.connections.insert(0, node)
        else:
            self.connections.append(node)
        node.connections.append(self)

    def remove_connection(self, node: Node) -> None:
        self.connections.remove(node)
        node.connections.remove(self)

    def set_connections(self, nodes: list[Node]) -> None:
        self.connections = nodes

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Node):
            return self.id == o.id

        return False

    def __lt__(self, o: Node) -> bool:
        return self.id < o.id

    def __hash__(self) -> int:
        return self.id

    def __repr__(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return str(self.id)
