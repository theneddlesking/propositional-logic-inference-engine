from src.knowledge_base import KnowledgeBase
from src.query import Query


class UnitTestResult:
    def __init__(self, name: str, description: str, algorithm_name: str, knowledge_base: KnowledgeBase, query: Query, expect, actual):
        self.name = name
        self.description = description

        self.algorithm_name = algorithm_name

        self.knowledge_base = knowledge_base
        self.query = query

        self.expect = expect
        self.actual = actual


        self.passed = expect == actual

    def __str__(self):
        passed_str = "PASSED" if self.passed else "FAILED"
        return f"{self.name} ({self.algorithm_name}) - {passed_str}\n{self.description}\n\nKB: {self.knowledge_base}\n\nQuery: {self.query}\n\nExpected: {self.expect.debug()}\n\nActual: {self.actual.debug()}\n"