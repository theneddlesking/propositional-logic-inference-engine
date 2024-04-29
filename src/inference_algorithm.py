from knowledge_base import KnowledgeBase
from query import Query

class InferenceAlgorithm:
    def __init__(self, name: str):
        self.name = name

    def run(self, knowledge_base: KnowledgeBase, query: Query):
        raise NotImplementedError()