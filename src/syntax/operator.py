from enum import Enum


class Operator(Enum):
    # NOTE: biconditional must be before implication because when checking for the string representation of the operator, it will match the implication operator first
    BICONDITIONAL = '<=>'

    IMPLICATION = '=>'
    AND = '&'
    NEGATION = '~'
    CONJUNCTION = '&'
    DISJUNCTION = '||'

    def __str__(self):
        return self.value