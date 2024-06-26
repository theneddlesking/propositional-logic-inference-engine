from src.algorithm_result import AlgorithmResult
from src.syntax.literal import Literal

class ChainingResult(AlgorithmResult):
    def __init__(self, algorithm_name: str, found: bool, entailed: set[Literal]):
        super().__init__(algorithm_name)
        self.found = found

        # order the symbols
        entailed = list(entailed)

        entailed.sort()

        entailed = set(entailed)

        self.entailed = entailed

    def __str__(self) -> str:
        # list of symbols that are entailed
        entailed_symbols = [str(symbol) for symbol in self.entailed]

        # str as a, b, c
        symbols_str = ", ".join(entailed_symbols)

        # yes or no
        found = "YES" if self.found else "NO"

        return f"{found}: {symbols_str}"

    def __eq__(self, other: 'ChainingResult') -> bool:
        return self.found == other.found and self.entailed == other.entailed