from src.syntax.sentence import AtomicSentence, Sentence
from src.syntax.literal import Literal


class KnowledgeBase:
    def __init__(self, sentences: list[Sentence] = None, propositional_symbols: set[Literal] = None):
        self.propositional_symbols = propositional_symbols if propositional_symbols is not None else set()
        self.sentences = sentences if sentences is not None else []

    def get_fact_literals(self) -> list[Literal]:
        sentences = self.sentences

        fact_sentences = [sentence for sentence in sentences if isinstance(sentence, AtomicSentence)]

        # map to literals
        fact_literals = [sentence.atom for sentence in fact_sentences]

        # they can be negated or not (eg. A and ~A are both valid)
        return fact_literals

    @classmethod
    def from_string(cls, string: str) -> 'KnowledgeBase':
        propositional_symbols = set()
        
        # remove all spaces in the string
        string = string.replace(" ", "")

        # remove all newlines in the string
        string = string.replace("\n", "")

        # split the string into sentences by ";"
        sentences = string.split(";")

        # remove any empty strings
        sentences = [sentence for sentence in sentences if sentence != ""]

        # get the actual sentences and update the propositional symbols set
        sentences = [Sentence.from_string(sentence, propositional_symbols) for sentence in sentences]

        return cls(sentences, propositional_symbols)
    
    def __str__(self):

        symbols = "\n".join([str(symbol) for symbol in self.propositional_symbols])

        sentences = "\n".join([str(sentence) for sentence in self.sentences])

        return f"Symbols:\n{symbols}\nSentences:\n{sentences}"