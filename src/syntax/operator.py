from enum import Enum


class Operator(Enum):
    IMPLICATION = '=>'
    AND = '&'
    NEGATION = '~'
    CONJUNCTION = '&'
    DISJUNCTION = '||'
    BICONDITIONAL = '<=>'
