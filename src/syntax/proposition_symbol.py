from src.syntax.atom import Atom
from src.syntax.utils import Utils


class PropositionSymbol(Atom):
    def __init__(self, symbol: str, value: bool = None):
        if not Utils.is_proposition_symbol(symbol):
            raise ValueError(f"{symbol} is not a valid propositional symbol. Should be a capital letter.")

        super().__init__(symbol, value)
       
    @classmethod
    def from_string(cls, string: str) -> 'PropositionSymbol':
        return cls(string)