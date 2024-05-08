from src.syntax.operator import Operator
from src.syntax.sentence import Sentence


class Expression(Sentence):
    def __init__(self, lhs: Sentence, operator: Operator, rhs: Sentence):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self):
        return f"{self.lhs} {self.operator} {self.rhs}"
    
    # TODO verify that this works, not sure
    @classmethod
    def from_string(cls, string: str) -> 'Expression':
        # find the operator
        operator = None
        for op in Operator:
            if op.value in string:
                operator = op
                break
        
        if operator is None:
            raise ValueError(f"Could not find an operator in {string}.")
        
        # split the string into lhs and rhs
        lhs, rhs = string.split(operator.value)
        
        return cls(Sentence.from_string(lhs), operator, Sentence.from_string(rhs))