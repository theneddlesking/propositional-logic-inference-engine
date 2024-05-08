# TODO I'm not sure how similar the forward and backward chaining algorithms are 
# but they have the same string output so I assume the actual outputs are the same? Not sure.

from src.algorithm_result import AlgorithmResult

# TODO implement the ChainingResult class
class ChainingResult(AlgorithmResult):
    def __init__(self, algorithm_name: str, found: bool, count: int):
        super().__init__(algorithm_name)
        self.found = found
        self.count = count

    def __str__(self) -> str:
        return f"{self.algorithm_name} found: {self.found}, count: {self.count}"