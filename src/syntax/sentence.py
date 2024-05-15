from src.model import Model
from src.syntax.atom import Atom, BoolAtom
from src.syntax.operator import Operator
from src.syntax.literal import Literal, PositiveLiteral
from src.syntax.utils import Utils


class Sentence:
    
    @classmethod
    def from_string(cls, string: str, dict: dict[str, Literal]) -> 'Sentence':

        print("bro im checking", string)
        print(len(string))
        # is the string a proposition symbol?
        if Utils.is_propositional_symbol(string) or Utils.is_negated_propositional_symbol(string):

            print("bro is a symbol", string)
            # get symbol from dict
            symbol = dict.get(string)

            if symbol is None:
                # create new symbol
                symbol = Literal.from_string(string)

            # add to dict
            dict[symbol.name] = symbol

            return AtomicSentence(symbol)
        
        # is the string a boolean value?
        if Utils.is_true_false(string):
            return AtomicSentence(BoolAtom.from_string(string))

        # otherwise this is a complex sentence
        return Expression.from_string(string, dict)
    
    # assumes that "A" is in A&B=>C and -A&B=>C
    def symbol_in_sentence(self, symbol: Literal) -> bool:
        return str(symbol) in str(self)
    
    def evaluate(self, model: Model) -> bool:
        raise NotImplementedError("Evaluate sbould be implemented in subclasses.")

class AtomicSentence(Sentence):
    def __init__(self, atom: Atom):
        super().__init__()
        self.atom = atom

    def __str__(self):
        return str(self.atom)
    
    def evaluate(self, model: Model) -> bool:
        # handle negation of the atom
        value_according_model = model.get(self.atom)

        # if the atom is negated, we need to negate the value according to the model
        if self.atom.negated:
            return not value_according_model
    
        return value_according_model

class Expression(Sentence):
    def __init__(self, lhs: Sentence, operator: Operator, rhs: Sentence):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self):
        return f"({self.lhs} {self.operator} {self.rhs})"
    
    @staticmethod
    def get_operator(string: str):
        # find the operator can be multiple chars long
        operator = None

        # we need to find the left most operator
        # so we need to find the index of the current operator and choose the one with the smallest index
        index = len(string)

        print("current string", string)

        for op in Operator:

            # skip negations because the literal handles that
            if op == Operator.NEGATION:
                continue

            # take the left most operator
            if op.value in string and string.index(op.value) < index:
                operator = op
                index = string.index(op.value)
        
        if operator is None:
            raise ValueError(f"Could not find an operator in {string}.")
        
        return operator
        
    # TODO add bracket ordering
    @classmethod
    def from_string(cls, string: str, dict: dict[str, Literal]) -> 'Expression':
        # get operator
        operator = cls.get_operator(string)
            
        # There are 3 bracket cases:
        # 1. (A&B)&C
        # 2. A&(B&C)
        # 3. A&(B&C)&D

        # Case 1 we want to group (A&B) as LHS and C as RHS
        # Case 2 we want to group A as LHS and (B&C) as RHS
        # Case 3 we want to group A as LHS and (B&C)&D as RHS

        # Case 2 is done by default because it already groups at operator left to right
        # Case 3 is done by default because it already groups at operator left to right

        # Therefore, we only need to handle Case 1

        # Case 1 is when the first operator is a bracket
        
        # if the first operator is a bracket then we need to group that as LHS
        if operator == Operator.OPENING_BRACKET:
            # get the first bracketed sentence
            opening_bracket_index = string.find(Operator.OPENING_BRACKET.value)

            # only if we find brackets
            if opening_bracket_index != -1:
                closing_bracket_index = Utils.find_matching_bracket(string, opening_bracket_index)

            # split the string into lhs and rhs at the closing bracket and ignore the opening bracket
            lhs = string[opening_bracket_index + 1:closing_bracket_index-1]
            rhs = string[closing_bracket_index + 1:]

            # if there is no rhs, then the expression is (A&B)
            if len(rhs) == 0:
                print(lhs, "moment")
                # so we just take the lhs
                return Sentence.from_string(lhs, dict)
            
             # between lhs and rhs there is an operator
            operator = string[closing_bracket_index]

            # convert to operator
            second_operator = Operator(operator)

            print("split string", string, "into ", lhs, "and", rhs)

            return cls(Sentence.from_string(lhs, dict), second_operator, Sentence.from_string(rhs, dict))
        
        # split the string into lhs and rhs at the first operator only
        lhs, rhs = string.split(operator.value, 1)
        
        return cls(Sentence.from_string(lhs, dict), operator, Sentence.from_string(rhs, dict))
    
    def evaluate(self, model: Model) -> bool:
        if self.operator == Operator.CONJUNCTION:
            return self.lhs.evaluate(model) and self.rhs.evaluate(model)
        
        if self.operator == Operator.DISJUNCTION:
            return self.lhs.evaluate(model) or self.rhs.evaluate(model)
        
        # A=>B is equivalent to -A or B according to material implication
        if self.operator == Operator.IMPLICATION:
            return not self.lhs.evaluate(model) or self.rhs.evaluate(model)
        
        # A<=>B is equivalent to (A=>B) and (B=>A) according to material equivalence
        # which is equivalent to (-A or B) and (-B or A) according to material implication
        if self.operator == Operator.BICONDITIONAL:
            return (not self.lhs.evaluate(model) or self.rhs.evaluate(model)) and (not self.rhs.evaluate(model) or self.lhs.evaluate(model))
        
        raise ValueError(f"Operator {self.operator} not supported.")

# Horn Clause implication form is always A & B & C => D with all positive literals, there cannot be any negative literals
# more info: https://stackoverflow.com/questions/45123756/why-do-we-call-a-disjunction-of-literals-of-which-none-is-positive-a-goal-clause

class HornClause(Expression):
    def __init__(self, body: list[PositiveLiteral], head: PositiveLiteral, dict: dict[str, Literal]):
        self.body = body
        self.head = head

        lhs = Sentence.from_string("&".join([str(literal) for literal in self.body]), dict)
        rhs = AtomicSentence(self.head)

        super().__init__(lhs, Operator.IMPLICATION, rhs)

    