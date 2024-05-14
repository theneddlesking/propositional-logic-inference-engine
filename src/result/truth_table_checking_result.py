from src.algorithm_result import AlgorithmResult
from src.syntax.literal import Literal

# TODO implement the TruthTableCheckingResult class
class TruthTableCheckingResult(AlgorithmResult):
    def __init__(self, models: list[dict[Literal, bool]], found: bool):
        super().__init__("TT")
        self.found = found
        self.models = models

    def __str__(self) -> str:
        models_str = ""

        # yes or no
        found = "YES" if self.found else "NO"

        return f"{found}: {models_str}"
