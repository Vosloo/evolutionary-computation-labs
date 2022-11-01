import numpy as np
import pandas as pd


class Instance:
    X = "x"
    Y = "y"
    COST = "cost"

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def get_coordinates(self) -> np.ndarray:
        return self.df[[self.X, self.Y]].to_numpy()
