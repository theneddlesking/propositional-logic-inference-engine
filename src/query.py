from src.syntax.sentence import Sentence


class Query:
    def __init__(self, sentence: 'Sentence'):
        self.sentence = sentence

    @classmethod
    def from_string(cls, string: str) -> 'Query':
        return cls(Sentence.from_string(string))