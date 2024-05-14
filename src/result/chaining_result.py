from src.algorithm_result import AlgorithmResult
from src.syntax.literal import Literal

class ChainingResult(AlgorithmResult):
    def __init__(self, algorithm_name: str, found: bool, entailed: list[Literal]):
        super().__init__(algorithm_name)
        self.found = found
        self.entailed = entailed

    def __str__(self) -> str:

        # list of symbols that are entailed
        entailed_symbols = [str(symbol) for symbol in self.entailed]

        # str as a, b, c
        symbols_str = ", ".join(entailed_symbols)

        # yes or no
        found = "YES" if self.found else "NO"

        return f"{found}: {symbols_str}"
