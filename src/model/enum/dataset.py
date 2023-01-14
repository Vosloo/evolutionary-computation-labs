from enum import Enum, unique


@unique
class Dataset(Enum):
    TSPA = "TSPA"
    TSPB = "TSPB"
    TSPC = "TSPC"
    TSPD = "TSPD"
