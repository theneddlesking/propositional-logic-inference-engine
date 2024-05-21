from src.model import Model
from src.syntax.atom import Atom, BoolAtom
from src.syntax.operator import Operator
from src.syntax.literal import Literal, PositiveLiteral
from src.syntax.utils import Utils

class Sentence:
    
    @classmethod
    def from_string(cls, string: str, known_symbols: set[Literal]) -> 'Sentence':
        # is the string a proposition symbol?
        if Utils.is_propositional_symbol(string) or Utils.is_negated_propositional_symbol(string):
            known_symbols.add(Literal.from_string(string))

            # atomic sentence needs to know if its negated or not
            return AtomicSentence(Literal.from_string(string))
        
        # is the string a boolean value?
        if Utils.is_true_false(string):
            return AtomicSentence(BoolAtom.from_string(string))

        # otherwise this is a complex sentence
        return Expression.from_string(string, known_symbols)
    
    def get_symbols(self) -> set[Literal]:
        raise NotImplementedError("Get symbols should be implemented in subclasses.")
    
    def evaluate(self, model: Model) -> bool:
        raise NotImplementedError("Evaluate should be implemented in subclasses.")
    
    def get_cnf(self) -> 'Sentence':
        raise NotImplementedError("Converting to CNF should be implemented in subclasses.")
    
    def convert_biconditionals(self) -> 'Sentence':
        raise NotImplementedError("Converting biconditionals should be implemented in subclasses.")

class AtomicSentence(Sentence):
    def __init__(self, atom: Atom):
        super().__init__()
        self.atom = atom

    def __str__(self):
        return str(self.atom)
    
    def evaluate(self, model: Model) -> bool:
        # handle negation of the atom
        value_according_model = model.get(self.atom.name)

        # if the atom is negated, we need to negate the value according to the model
        if self.atom.negated:
            return not value_according_model
    
        return value_according_model
    
    def get_symbols(self) -> set[Literal]:
        return set([self.atom])
    
    def get_cnf(self) -> Sentence:
        return self
    
    def convert_biconditionals(self) -> Sentence:
        return self

class Expression(Sentence):
    def __init__(self, lhs: Sentence, operator: Operator, rhs: Sentence):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self):
        # if operator is negation then only show the rhs
        if self.operator == Operator.NEGATION:
            return f"{self.operator}{self.rhs}"

        return f"({self.lhs} {self.operator} {self.rhs})"
    
    @staticmethod
    def get_operator(string: str):
        # find the operator can be multiple chars long
        operator = None

        # we need to find the left most operator
        # so we need to find the index of the current operator and choose the one with the smallest index
        index = len(string)

        for op in Operator:
            # take the left most operator
            if op.value in string and string.index(op.value) < index:
                operator = op
                index = string.index(op.value)
        
        if operator is None:
            raise ValueError(f"Could not find an operator in {string}")
        
        return operator
        
    @classmethod
    def from_string(cls, string: str, known_symbols: set[Literal]) -> 'Expression':
        # get operator
        operator = cls.get_operator(string)

        # if its a negation check if the next character is a bracket because it could be a negated sentence
        if operator == Operator.NEGATION:
            negation_index = string.find(Operator.NEGATION.value)

            negation_length = len(Operator.NEGATION.value)

            next_char_is_bracket = string[negation_index + negation_length] == Operator.OPENING_BRACKET.value

            # negated literal
            if not next_char_is_bracket:
                # if its not a bracket then we need to find the next operator because the negation is only for the next literal
                operator = cls.get_operator(string[(negation_index + negation_length):])

            # negated sentence
            else:
                # TODO: refactor, this shit is too similar to opening bracket below
                # we need to negate this sentence
                opening_bracket_index = string.find(Operator.OPENING_BRACKET.value)
                closing_bracket_index = Utils.find_matching_bracket(string, opening_bracket_index)

                operator_substring = string[closing_bracket_index:]

                # if there is no rhs, then the expression could be e.g. ~(A&B)
                if len(operator_substring) == 0:
                    # so we just take the lhs
                    # index is 2 because we need to skip over negation and opening bracket
                    return Sentence.from_string(string[2:-1], known_symbols)
                
                # get the next operator after the closing bracket
                second_operator = cls.get_operator(operator_substring)

                # first part: get the local index of the second operator in the operator substring
                # second part: add the index of where it is in the actual string
                second_operator_index = operator_substring.find(second_operator.value) + (len(string) - len(operator_substring))

                # lhs_string is everything before the second operator index
                # rhs_string is everything after the second operator index plus the operator's length
                lhs_string = string[opening_bracket_index:second_operator_index]
                rhs_string = string[second_operator_index + len(second_operator.value):]

                lhs = Sentence.from_string(lhs_string, known_symbols)
                rhs = Sentence.from_string(rhs_string, known_symbols)

                negated_sentence = Expression(None, Operator.NEGATION, lhs)

                return Expression(negated_sentence, second_operator, rhs)
            
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

            # between lhs and rhs there is an operator
            # but the operator could be 1 length, 2 length of 3 length
            # so we need the substring to find the operator
            # find the operator
            operator_substring = string[closing_bracket_index:]

            # if there is no rhs, then the expression could be e.g. (A&B)
            if len(operator_substring) == 0:
                # so we just take the lhs
                return Sentence.from_string(string[1:-1], known_symbols)
            
            # get the next operator after the closing bracket
            second_operator = cls.get_operator(operator_substring)

            # first part: get the local index of the second operator in the operator substring
            # second part: add the index of where it is in the actual string
            second_operator_index = operator_substring.find(second_operator.value) + (len(string) - len(operator_substring))

            # lhs is everything before the second operator index
            # rhs is everything after the second operator index plus the operator's length
            lhs = string[:second_operator_index]
            rhs = string[second_operator_index + len(second_operator.value):]

            return cls(Sentence.from_string(lhs, known_symbols), second_operator, Sentence.from_string(rhs, known_symbols))
        
        # split the string into lhs and rhs at the first operator only
        lhs, rhs = string.split(operator.value, 1)
        
        return cls(Sentence.from_string(lhs, known_symbols), operator, Sentence.from_string(rhs, known_symbols))
    
    def evaluate(self, model: Model) -> bool:
        if self.operator == Operator.NEGATION:
            return not self.rhs.evaluate(model)

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
    
    def get_symbols(self) -> set[Literal]:
        return self.lhs.get_symbols().union(self.rhs.get_symbols())
    
    def get_cnf(self) -> Sentence:
        # eliminate biconditionals and implications
        # replace A <=> B with (A => B) & (B => A)
        # replace A => B with ~A || B
        sentence = self.convert_biconditionals()
        print(sentence)
        sentence = self.convert_implications()

        # move negations inward (negation normal form)
        # apply de morgan's laws
        # ~(A & B) === ~A || ~B
        # ~(A || B) === ~A & ~B
        # eliminate double negations
        # ~(~A) === A
        sentence = self.apply_de_morgans_laws()
        sentence = self.remove_double_negations()

        # distribute disjunctions over conjunctions
        # apply the distributive law to move disjunctions inside conjunctions
        # A || (B & C) === (A || B) & (A || C)
        sentence = self.distribute_conjuctions_over_disjunctions()
        return sentence
    
    def convert_biconditionals(self) -> Sentence:
        # negation expression doesn't have a lhs
        if self.operator != Operator.NEGATION:
            self.lhs = self.lhs.convert_biconditionals()
        self.rhs = self.rhs.convert_biconditionals()

        # this isn't an infinite loop, the atomic sentence has the base case
        if self.operator == Operator.BICONDITIONAL:
            # split the biconditional using the following rule:
            # A <=> B === (A => B) & (B => A)
            implication_lhs = Expression(self.lhs, Operator.IMPLICATION, self.rhs)
            implication_rhs = Expression(self.rhs, Operator.IMPLICATION, self.lhs)
            return Expression(implication_lhs, Operator.AND, implication_rhs)
    
        return self

    def convert_implications(self) -> Sentence:
        pass

    def apply_de_morgans_laws(self) -> Sentence:
        # also group the sentences
        pass

    def remove_double_negations(self) -> Sentence:
        pass

    def distribute_conjuctions_over_disjunctions(self) -> Sentence:
        pass

# Horn Clause implication form is always A & B & C => D with all positive literals, there cannot be any negative literals
# more info: https://stackoverflow.com/questions/45123756/why-do-we-call-a-disjunction-of-literals-of-which-none-is-positive-a-goal-clause

class HornClause(Expression):
    def __init__(self, body: list[PositiveLiteral], head: PositiveLiteral, known_symbols: set[Literal]):
        self.body = body
        self.head = head

        lhs = Sentence.from_string("&".join([str(literal) for literal in self.body]), known_symbols)
        rhs = AtomicSentence(self.head)

        super().__init__(lhs, Operator.IMPLICATION, rhs)
        
    @staticmethod
    def get_symbols(sentence: Sentence, body: list[PositiveLiteral]) -> list[PositiveLiteral]:
        # if sentence is expression make sure operator is conjunction or implication
        if isinstance(sentence, Expression):
            # if it is the last sentence
            last_sentence = isinstance(sentence.rhs, AtomicSentence)

            # then the last sentence needs to be implication
            if not last_sentence and sentence.operator != Operator.CONJUNCTION:
                raise ValueError(f"Body of Horn clause must be conjunctions only.", str(sentence))
            
            # else it has to be a conjunction
            if last_sentence and sentence.operator != Operator.IMPLICATION:
                raise ValueError(f"Head of Horn clause must be implication only.", str(sentence))

        # add lhs
        if isinstance(sentence.lhs, AtomicSentence):
            # check if its a positive literal
            if sentence.lhs.atom.negated:
                raise ValueError(f"Body of Horn clause must be positive literals only.", str(sentence)) 
    
            body.append(sentence.lhs.atom)
        
        # add rhs
        if isinstance(sentence.rhs, AtomicSentence):
            # check if its a positive literal
            if sentence.lhs.atom.negated:
                raise ValueError(f"Body of Horn clause must be positive literals only.", str(sentence)) 
            
            body.append(sentence.rhs.atom)
        else:
            HornClause.get_symbols(sentence.rhs, body)
        
        return body

    @classmethod
    def from_expression(cls, sentence: Expression, known_symbols: set[Literal]) -> 'HornClause':
        # get symbols
        all_symbols = cls.get_symbols(sentence, [])

        # get head
        head = all_symbols.pop()

        # get body
        body = all_symbols

        return cls(body, head, known_symbols)
    
    def __str__(self):
        return f"{' & '.join([str(literal) for literal in self.body])} => {self.head}"