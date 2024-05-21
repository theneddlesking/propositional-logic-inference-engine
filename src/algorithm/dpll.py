from src.cnf_knowledge_base import CNFKnowledgeBase
from src.inference_algorithm import InferenceAlgorithm
from src.query import Query
from src.result.dpll_result import DPLLResult


class DPLL(InferenceAlgorithm):

    def __init__(self):
        super().__init__("DPLL")

    def run(self, knowledge_base: CNFKnowledgeBase, query: Query) -> DPLLResult:
        pass
