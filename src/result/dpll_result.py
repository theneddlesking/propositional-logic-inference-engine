from src.algorithm_result import AlgorithmResult

class DPLLResult(AlgorithmResult):
    def __init__(self):
        super().__init__("DPLL")

    def __str__(self) -> str:
        pass
    
    def __eq__(self, other: 'DPLLResult') -> bool:
        pass