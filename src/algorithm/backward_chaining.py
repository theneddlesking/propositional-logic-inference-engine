from src.horn_knowledge_base import HornKnowledgeBase
from src.inference_algorithm import InferenceAlgorithm
from src.query import HornKnowledgeBaseQuery
from src.result.chaining_result import ChainingResult
from src.syntax.literal import PositiveLiteral

class BackwardChaining(InferenceAlgorithm):
    def __init__(self):
        super().__init__("BC")

    def run(self, knowledge_base: HornKnowledgeBase, query: HornKnowledgeBaseQuery) -> ChainingResult:
        # ultimate goal
        goal = query.positive_literal

        # entailed symbols
        entailed = set()

        # do the backward chaining recursively
        found = self.backwards_chaining(knowledge_base, goal, entailed)

        if found:
            return ChainingResult(self.name, True, entailed)
        
        return ChainingResult(self.name, False, entailed)

    def backwards_chaining(self, knowledge_base: HornKnowledgeBase, goal: PositiveLiteral, entailed: set[PositiveLiteral]) -> bool:
        # if the goal is already a fact
        if goal in knowledge_base.facts:
            return True
        
        # check if any rule has the goal as the head
        for rule in knowledge_base.rules:
            if rule.head == goal:
                # check if all the symbols in the body are entailed
                if all([self.backwards_chaining(knowledge_base, symbol, entailed) for symbol in rule.body]):
                        entailed.add(goal)
                        return True