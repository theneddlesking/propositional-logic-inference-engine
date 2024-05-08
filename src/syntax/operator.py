from enum import Enum


class Operator(Enum):
    IMPLICATION = '=>'
    AND = '&'
    NEGATION = '~'
    CONJUNCTION = '&'
    DISJUNCTION = '||'
    BICONDITIONAL = '<=>'

    def __str__(self):
        return self.value