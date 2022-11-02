from dataclasses import dataclass
from statistics import mean

from src.model import Run


@dataclass
class Grade:
    def __init__(
        self, method_name: str, best_run: Run, runs: list[Run]
    ) -> None:
        self.method_name = method_name
        self.best_run: Run = best_run
        self.runs = runs

        scores = [run.score for run in runs]
        self.min: float = min(scores)
        self.max: float = max(scores)
        self.avg: float = mean(scores)

    def __repr__(self) -> str:
        return (
            f"\n{' Grade ':=^80}"
            f"\n{'Method:':<40}{self.method_name}"
            f"\n{'Best run id:':<40}{self.best_run.id}"
            f"\n{'Best run cost:':<40}{self.best_run.cost}"
            f"\n{'Best run distance:':<40}{self.best_run.distance}"
            f"\n{'Best run score:':<40}{self.best_run.score}"
            f"\n{'Min score:':<40}{self.min}"
            f"\n{'Avg score:':<40}{self.avg}"
            f"\n{'Max score:':<40}{self.max}"
            f"\n{'':=^80}\n"
        )
