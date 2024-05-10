from src.syntax.literal import Literal
from src.syntax.sentence import Sentence


class Query:
    def __init__(self, sentence: 'Sentence'):
        self.sentence = sentence

    @classmethod
    def from_string(cls, string: str, dict: dict[str, Literal]) -> 'Query':
        return cls(Sentence.from_string(string, dict))