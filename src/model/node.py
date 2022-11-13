from __future__ import annotations


class Node:
    def __init__(self, id, x, y, cost) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.cost = cost
        self.connections: list[Node] = []

    def add_connection(self, node: Node) -> None:
        self.connections.append(node)
        node.connections.append(self)

    def remove_connection(self, node: Node) -> None:
        self.connections.remove(node)
        node.connections.remove(self)

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
