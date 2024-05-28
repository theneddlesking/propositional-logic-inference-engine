from src.knowledge_base import KnowledgeBase
from src.query import Query
from src.algorithm_result import AlgorithmResult


class InferenceAlgorithm:
    def __init__(self, name: str):
        self.name = name

    def run(self, knowledge_base: KnowledgeBase, query: Query) -> "AlgorithmResult":
        raise NotImplementedError()
