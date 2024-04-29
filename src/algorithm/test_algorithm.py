from src.algorithm_result import AlgorithmResult
from src.inference_algorithm import InferenceAlgorithm
from src.knowledge_base import KnowledgeBase
from src.query import Query
from src.result.test_result import TestResult

# this is not a real algorithm and is only used for testing purposes
class TestAlgorithm(InferenceAlgorithm):
    def __init__(self):
        super().__init__("TEST")

    def run(self, knowledge_base: KnowledgeBase, query: Query) -> AlgorithmResult:
        return TestResult()