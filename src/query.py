from src.syntax.literal import Literal, PositiveLiteral
from src.syntax.sentence import AtomicSentence, Sentence


class Query:
    def __init__(self, sentence: 'Sentence'):
        self.sentence = sentence

    @classmethod
    def from_string(cls, string: str, dict: dict[str, Literal]) -> 'Query':
        return cls(Sentence.from_string(string, dict))
    
class HornKnowledgeBaseQuery(Query):
    def __init__(self, positive_literal: PositiveLiteral) -> None:
        sentence = AtomicSentence(positive_literal)
        super().__init__(sentence)

        self.positive_literal = positive_literal
