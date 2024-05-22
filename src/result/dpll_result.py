from src.algorithm_result import AlgorithmResult
from src.cnf_knowledge_base import CNFKnowledgeBase

class DPLLResult(AlgorithmResult):
    def __init__(self, satisfiable: bool, knowledge_base: CNFKnowledgeBase):
        super().__init__("DPLL")
        self.satisfiable = satisfiable
        self.knowledge_base = knowledge_base

    def __str__(self) -> str:
        yes_no_str = "YES" if self.satisfiable else "NO"
        return f"{yes_no_str}"
    
    def __eq__(self, other: 'DPLLResult') -> bool:
        return self.satisfiable == other.satisfiable
    
    def debug(self) -> str:
        string = self.__str__()

        # if its a test result, there is no knowledge base
        if self.knowledge_base is None:
            return string

        string += "\n"
        string += "\n"

        string += "DPLL Knowledge Base:\n"

        for clause in self.knowledge_base.clauses:
            string += f"{clause}\n"

        return string

