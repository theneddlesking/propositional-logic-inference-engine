from src.syntax.atom import BoolAtom
from src.syntax.atomic_sentence import AtomicSentence
from src.syntax.expression import Expression
from src.syntax.proposition_symbol import PropositionSymbol


class Sentence:
    
    @classmethod
    def from_string(cls, string: str) -> 'Sentence':
        # is the string a proposition symbol?
        if Sentence.is_proposition_symbol(string):
            return AtomicSentence(PropositionSymbol.from_string(string))
        
        # is the string a boolean value?
        if Sentence.is_true_false(string):
            return AtomicSentence(BoolAtom.from_string(string))

        # otherwise this is a complex sentence
        return Expression.from_string(string)

    @staticmethod
    def is_atom(string: str) -> bool:
        return Sentence.is_proposition_symbol(string) or Sentence.is_true_false(string)

    @staticmethod
    def is_proposition_symbol(string: str) -> bool:
        return string.isalpha() and string.isupper() and len(string) == 1
    
    @staticmethod
    def is_true_false(string: str) -> bool:
        return string == "True" or string == "False"