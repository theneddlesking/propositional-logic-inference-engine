from src.syntax.atom import Atom, BoolAtom
from src.syntax.operator import Operator
from src.syntax.proposition_symbol import PropositionSymbol
from src.syntax.utils import Utils


class Sentence:
    
    @classmethod
    def from_string(cls, string: str, dict: dict[str, PropositionSymbol]) -> 'Sentence':
        # is the string a proposition symbol?
        if Utils.is_proposition_symbol(string):

            # get symbol from dict
            symbol = dict.get(string)

            if symbol is None:
                # create new symbol
                symbol = PropositionSymbol.from_string(string)

            # add to dict
            dict[symbol.name] = symbol

            return AtomicSentence(symbol)
        
        # is the string a boolean value?
        if Utils.is_true_false(string):
            return AtomicSentence(BoolAtom.from_string(string))

        # otherwise this is a complex sentence
        return Expression.from_string(string, dict)
    
    # TODO kinda hacky, but it works
    def symbol_in_sentence(self, symbol: PropositionSymbol) -> bool:
        return str(symbol) in str(self)

class AtomicSentence(Sentence):
    def __init__(self, atom: Atom):
        super().__init__()
        self.atom = atom

    def __str__(self):
        return str(self.atom)

class Expression(Sentence):
    def __init__(self, lhs: Sentence, operator: Operator, rhs: Sentence):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self):
        return f"{self.lhs} {self.operator} {self.rhs}"
    
    # TODO verify that this works, not sure
    @classmethod
    def from_string(cls, string: str, dict: dict[str, PropositionSymbol]) -> 'Expression':
        # find the operator can be multiple chars long
        operator = None
        for op in Operator:
            if op.value in string:
                operator = op
                break
        
        if operator is None:
            raise ValueError(f"Could not find an operator in {string}.")
        
        # split the string into lhs and rhs at the first operator only
        lhs, rhs = string.split(operator.value, 1)
        
        return cls(Sentence.from_string(lhs, dict), operator, Sentence.from_string(rhs, dict))
    