from random import sample, seed

from src.model import Node
from src.utils import sort_connections


def random_sequence(nodes: list[Node], node_coverage: int, **kwargs) -> list[Node]:
    # seed(8888)
    return sort_connections(sample(nodes, node_coverage))
