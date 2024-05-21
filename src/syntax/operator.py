from enum import Enum


class Operator(Enum):
    BICONDITIONAL = '<=>'

    IMPLICATION = '=>'
    NEGATION = '~'
    CONJUNCTION = '&'
    DISJUNCTION = '||'

    OPENING_BRACKET = '('
    CLOSING_BRACKET = ')'

    def __str__(self):
        return self.value