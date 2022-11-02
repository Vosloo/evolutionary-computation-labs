import numpy as np
import pandas as pd


class Instance:
    X = "x"
    Y = "y"
    COST = "cost"

    def __init__(self, instance_name: str, df: pd.DataFrame) -> None:
        self.instance_name = instance_name
        self.df = df
        self.x = df[self.X]
        self.y = df[self.Y]
        self.cost = df[self.COST]

    def get_coordinates(self) -> np.ndarray:
        return self.df[[self.X, self.Y]].to_numpy()
