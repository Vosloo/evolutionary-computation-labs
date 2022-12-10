from __future__ import annotations


class Node:
    def __init__(self, id, x, y, cost) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.cost = cost
        self.next_connection: Node = None
        self.prev_connection: Node = None

    def add_prev_connection(self, node: Node) -> Node:
        if self.prev_connection is not None or node.next_connection is not None:
            raise ValueError("Nodes already have connections!")

        self.prev_connection = node
        node.next_connection = self

        return self

    def add_next_connection(self, node: Node) -> Node:
        if self.next_connection is not None or node.prev_connection is not None:
            raise ValueError("Nodes already have connections!")

        self.next_connection = node
        node.prev_connection = self

        return self

    def remove_connection(self, node: Node) -> Node:
        if node == self.next_connection:
            self.next_connection = None
            node.prev_connection = None
        elif node == self.prev_connection:
            self.prev_connection = None
            node.next_connection = None
        else:
            raise ValueError("Node is not connected to this node")

        return self

    def reverse_connections(self) -> None:
        """Reverses the order of the connections in place"""
        self.next_connection, self.prev_connection = self.prev_connection, self.next_connection

    @property
    def connections(self) -> list[Node]:
        return [self.prev_connection, self.next_connection]

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
