from random import sample

from src.model import Node



def random(nodes: list[Node], node_coverage: int, **kwargs) -> list[Node]:
    return sample(nodes, node_coverage)
