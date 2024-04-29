# standard result object for the algorithm output
# useful for testing and debugging later

class AlgorithmResult:
    def __init__(self, algorithm_name: str):
        self.algorithm_name = algorithm_name

    def __str__(self) -> str:
        raise NotImplementedError("This method must be implemented by the subclass.")
