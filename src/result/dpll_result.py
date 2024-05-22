from src.algorithm_result import AlgorithmResult

class DPLLResult(AlgorithmResult):
    def __init__(self, satisfiable: bool):
        super().__init__("DPLL")
        self.satisfiable = satisfiable

    def __str__(self) -> str:
        yes_no_str = "YES" if self.satisfiable else "NO"
        return f"{yes_no_str}"
    
    def __eq__(self, other: 'DPLLResult') -> bool:
        return self.satisfiable == other.satisfiable