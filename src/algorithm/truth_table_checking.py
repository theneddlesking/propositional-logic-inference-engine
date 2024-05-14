from src.horn_knowledge_base import HornKnowledgeBase
from src.inference_algorithm import InferenceAlgorithm
from src.query import HornKnowledgeBaseQuery
from src.result.chaining_result import ChainingResult
from src.syntax.literal import PositiveLiteral

# TODO implement the TruthTableChecking class
class TruthTableChecking(InferenceAlgorithm):
    def __init__(self):
        super().__init__("TT")

    def run(self, knowledge_base: HornKnowledgeBase, query: HornKnowledgeBaseQuery) -> ChainingResult:
        # ultimate goal
        goal = query.positive_literal
    