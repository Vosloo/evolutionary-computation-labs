from src.model import Node
from random import sample

def random(pivot_node: Node, nodes: list[Node], node_coverage: int, **kwargs) -> list[Node]:
    return sample(nodes, node_coverage)
