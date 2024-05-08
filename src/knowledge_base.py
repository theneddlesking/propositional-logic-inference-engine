from src.syntax.sentence import Sentence
from src.syntax.proposition_symbol import PropositionSymbol


class KnowledgeBase:
    # TODO implement knowledge base, figure out what properties and methods are needed
    def __init__(self, propositional_symbols: dict[str, PropositionSymbol] = None, sentences: list[Sentence] = None):
        self.propositional_symbols = propositional_symbols
        self.sentences = sentences if sentences is not None else []

    @classmethod
    def from_string(cls, string: str) -> 'KnowledgeBase':
        propositional_symbols = {}
        
        # remove all spaces in the string
        string = string.replace(" ", "")

        # remove all newlines in the string
        string = string.replace("\n", "")

        # split the string into sentences by ";"
        sentences = string.split(";")

        # remove any empty strings
        sentences = [sentence for sentence in sentences if sentence != ""]

        # get the actual sentences
        sentences = [Sentence.from_string(sentence, propositional_symbols) for sentence in sentences]

        return cls(sentences, propositional_symbols)
    
    def __str__(self):
        return "\n".join([str(sentence) for sentence in self.sentences])