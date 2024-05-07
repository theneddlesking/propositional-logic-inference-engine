from src.operator import Operator


class Expression:
    def __init__(self, lhs, operator: Operator, rhs):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self):
        return f"{self.lhs} {self.operator} {self.rhs}"