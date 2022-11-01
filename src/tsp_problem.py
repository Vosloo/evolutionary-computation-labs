from src.data_loader import DataLoader


class TSPProblem:
    def __init__(self) -> None:
        self.instances = DataLoader.load_tsp_instances()
