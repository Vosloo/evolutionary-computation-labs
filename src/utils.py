from src.model import Node

TYPE_EDGES = list[tuple[Node, Node]]


def get_edges(nodes: list[Node]) -> TYPE_EDGES:
    if len(nodes) < 2:
        raise ValueError("There must be at least 2 nodes to get edges")

    if len(nodes) == 2:
        return [(nodes[0], nodes[1])]

    return [(curr_node, curr_node.next_connection) for curr_node in nodes]


def linked_to_sequence(starting_node: Node) -> list[Node]:
    sequence = []
    current_node = starting_node

    while True:
        sequence.append(current_node)
        current_node = current_node.next_connection
        if current_node is None:
            raise ValueError("current_node is None")

        if current_node == starting_node:
            break

    return sequence


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

    return sort_connections(sequence)


def sort_connections(nodes: list[Node]) -> list[Node]:
    for i in range(1, len(nodes)):
        curr_node = nodes[i]
        prev_node = nodes[i - 1]
        curr_node.add_prev_connection(prev_node)

    nodes[-1].add_next_connection(nodes[0])

    return nodes


def find_nodes_in_sequence(nodes: list[Node], sequence: list[Node]) -> list[int | None]:
    node_idx = [None] * len(nodes)

    for i, curr_node in enumerate(sequence):
        for j, node in enumerate(nodes):
            if curr_node == node:
                node_idx[j] = i
                break

        if all([ind is not None for ind in node_idx]):
            break
    else:
        raise ValueError("Not all indices were found!")

    return node_idx
