from src.model import Node

TYPE_EDGES = list[tuple[Node, Node]]


def get_edges(nodes: list[Node]) -> TYPE_EDGES:
    edges = []
    visited_nodes = set()
    for node in nodes:
        for connection in node.connections:
            if connection not in visited_nodes:
                edges.append((node, connection))

        visited_nodes.add(node)

    return edges


def nodes_to_sequence(nodes: list[Node]) -> list[Node]:
    sequence = []
    visited_nodes = set()
    stack = [nodes[0]]
    while stack:
        node = stack.pop(0)
        if node in visited_nodes:
            continue

        sequence.append(node)
        visited_nodes.add(node)

        for connection in node.connections:
            if connection in visited_nodes:
                continue

            stack.insert(0, connection)
    return sequence


if __name__ == "__main__":
    nodes: list[Node] = []
    for i in range(1, 7):
        nodes.append(Node(i, 0, 0, 0))
    
    for i in range(len(nodes) - 1):
        node = nodes[i]

        node.add_connection(nodes[i + 1])

    print(nodes_to_sequence(nodes))
