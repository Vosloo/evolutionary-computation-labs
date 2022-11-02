from os import listdir

import pandas as pd
from definitions import ROOT_DIR

from src.model import Instance
from pathlib import Path

CSV_SEP = ";"


class DataLoader:
    @staticmethod
    def load_tsp_instances() -> dict[Instance]:
        """Load the TSP instances from the data folder.

        Returns:
            list[Instance]: List of Instance objects containing the TSP instances.
        """
        data_path = ROOT_DIR / "data"
        data_files = [f for f in listdir(data_path) if f.endswith(".csv")]

        instances = {}
        for file in data_files:
            path = Path(data_path / file)
            instances[path.stem] = Instance(
                path.stem,
                pd.read_csv(
                    str(path),
                    sep=CSV_SEP,
                    header=None,
                    names=[Instance.X, Instance.Y, Instance.COST],
                ),
            )

        return instances
