from src.model import Model
from src.syntax.literal import Literal


class CNFClause:
    def __init__(self, literals: list[Literal]):
        self.literals = literals

    def satisfies(self, model: Model) -> bool:
        return any(literal.satifies(model) for literal in self.literals)

    def is_unit_clause(self) -> bool:
        return len(self.literals) == 1

    def is_empty(self) -> bool:
        return len(self.literals) == 0

    def simplify(self, model: Model) -> "CNFClause":
        return CNFClause(
            [literal for literal in self.literals if (model.get(literal.name) != False)]
        )

    def is_tautology(self) -> bool:
        for symbol in self.literals:
            if Literal(symbol.name, not symbol.negated) in self.literals:
                return True
        return False

    def __str__(self):
        return f"{' || '.join([str(literal) for literal in self.literals])}"

    def __eq__(self, other: "CNFClause"):
        return self.literals == other.literals

    def copy(self) -> "CNFClause":
        return CNFClause(
            [Literal.from_string(str(literal)) for literal in self.literals]
        )

    def from_string(string: str) -> "CNFClause":
        literals = string.split(" || ")
        return CNFClause([Literal.from_string(literal) for literal in literals])
