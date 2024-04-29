from src.algorithm_result import AlgorithmResult

# this is not a real result from a real algorithm and is only used for testing purposes
class TestResult(AlgorithmResult):
    def __init__(self):
        super().__init__("TEST")

    def __str__(self) -> str:
        return "The test algorithm ran correctly, and a result was created."