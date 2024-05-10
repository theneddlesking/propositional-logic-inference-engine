from src.syntax.atom import Atom
from src.syntax.operator import Operator
from src.syntax.utils import Utils

class Literal(Atom):
    def __init__(self, symbol: str, negated = False):
        if not Utils.is_propositional_symbol(symbol):
            raise ValueError(f"{symbol} is not a valid propositional symbol. Should be a capital letter.")

        super().__init__(symbol, negated)
       
    @classmethod
    def from_string(cls, string: str) -> 'Literal':    
        # check if the string is negated
        if string[0] == Operator.NEGATION.value:
            return cls(string[1:], True)
        
        # no negation
        return cls(string, False)
