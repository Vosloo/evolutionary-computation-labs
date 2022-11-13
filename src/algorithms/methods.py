from enum import Enum, unique


@unique
class Method(Enum):
    RANDOM = "random"
    NEAREST = "nearest"
    GREEDY_CYCLE = "greedy_cycle"
    GREEDY_REGRET = "greedy_regret"
    GREEDY_REGRET_WEIGHTED = "greedy_regret_weighted"
