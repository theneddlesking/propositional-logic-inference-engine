from src.syntax.operator import Operator


class Atom:
    def __init__(self, name: str, negated = False):
        self.name = name
        self.negated = negated

    def __str__(self):
        return f"{Operator.NEGATION.value if self.negated else ''}{self.name}"
    
class BoolAtom(Atom):
    def __init__(self, bool: bool):
        name = "True" if bool else "False"
        super().__init__(name, bool)

    @classmethod
    def from_string(cls, string: str) -> 'BoolAtom':
        # needs to be True or False
        if string != "True" and string != "False":
            raise ValueError(f"{string} is not a valid boolean value. Should be True or False.")

        return cls(string == "True")