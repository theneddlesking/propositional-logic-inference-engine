from src.algorithm_result import AlgorithmResult
from src.syntax.literal import Literal

class TruthTableCheckingResult(AlgorithmResult):
    def __init__(self, models: list[dict[Literal, bool]], found: bool):
        super().__init__("TT")
        self.found = found
        self.models = models

    def __str__(self) -> str:
        # yes or no
        found = "YES" if self.found else "NO"

        number_of_models = len(self.models)

        return f"{found}: {number_of_models}"
