from src.cnf_knowledge_base import CNFKnowledgeBase
from src.inference_algorithm import InferenceAlgorithm
from src.query import Query
from src.result.dpll_result import DPLLResult


class DPLL(InferenceAlgorithm):

    def __init__(self):
        super().__init__("DPLL")

    def run(self, knowledge_base: CNFKnowledgeBase, query: Query) -> DPLLResult:
        satisifable = self.dpll(knowledge_base)
        return DPLLResult(satisifable)        

    def dpll(self, cnf: CNFKnowledgeBase) -> bool:
        
        while cnf.has_unit_clause():
            cnf = cnf.unit_propagate()

        while cnf.has_pure_symbol():
            cnf = cnf.pure_symbol_assign()

        if cnf.is_empty():
            return True
        
        if cnf.has_empty_clause():
            return False
        
        # choose a symbol
        p = cnf.choose_symbol()

        # create a new knowledge base with p assigned true
        knowledge_base_true = cnf.copy()

        knowledge_base_true.assign(p, True)

        # create a new knowledge base with p assigned false
        knowledge_base_false = cnf.copy()

        knowledge_base_false.assign(p, False)

        return self.dpll(knowledge_base_true) or self.dpll(knowledge_base_false)
    
