from src.inference_algorithm import InferenceAlgorithm
from src.knowledge_base import KnowledgeBase
from src.query import Query

# TODO implement the BackwardChaining class
class BackwardChaining(InferenceAlgorithm):
    def __init__(self):
        super().__init__("BC")

    # NOTE: Query is always a single positive literal

    def run(self, knowledge_base: KnowledgeBase, query: Query):
        # TODO implement the backward chaining algorithm        
        pass
