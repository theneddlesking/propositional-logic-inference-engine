from src.model import Model
from src.syntax.atom import Atom
from src.syntax.operator import Operator
from src.syntax.utils import Utils


class Literal(Atom):
    def __init__(self, symbol: str, negated=False):
        if not Utils.is_propositional_symbol(symbol):
            raise ValueError(f"{symbol} is not a valid propositional symbol.")

        super().__init__(symbol, negated)

    def __lt__(self, other: "Literal"):
        return self.name < other.name

    def __str__(self):
        return f"{Operator.NEGATION.value if self.negated else ''}{self.name}"

    @classmethod
    def from_string(cls, string: str) -> "Literal":
        # check if the string is negated
        if string[0] == Operator.NEGATION.value:
            return cls(string[1:], True)

        # no negation
        return cls(string, False)

    def satifies(self, model: Model) -> bool:
        model_value = model.get(self.name)

        # the model should contain a value for the literal
        if model_value is None:
            return False

        return model_value != self.negated


class PositiveLiteral(Literal):
    def __init__(self, symbol: str):
        super().__init__(symbol, False)
