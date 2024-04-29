# standard result object for the algorithm output
# useful for testing and debugging later

class AlgorithmResult:
    def __init__(self, algorithm_name: str):
        self.algorithm_name = algorithm_name

    def __str__(self) -> str:
        raise NotImplementedError("__str__ method must be implemented by the subclass.")

    def __eq__(self, other: 'AlgorithmResult') -> bool:
        raise NotImplementedError("__eq__ method must be implemented by the subclass.")