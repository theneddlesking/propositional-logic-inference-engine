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
    
    def get_cnfs(self) -> 'Sentence':
        raise NotImplementedError("Converting to CNF should be implemented in subclasses.")
    
    def convert_biconditionals(self) -> 'Sentence':
        raise NotImplementedError("Converting biconditionals should be implemented in subclasses.")
    
    def convert_implications(self) -> 'Sentence':
        raise NotImplementedError("Converting implications should be implemented in subclasses.")
    
    def remove_double_negations(self) -> 'Sentence':
        raise NotImplementedError("Removing double negations should be implemented in subclasses.")
    
    def apply_de_morgans_laws(self) -> 'Sentence':
        raise NotImplementedError("Applying De Morgan's laws should be implemented in subclasses.")
    
    def distribute_conjuctions_over_disjunctions(self) -> 'Sentence':
        raise NotImplementedError("Distributing conjunctions over disjunctions should be implemented in subclasses.")
    
    def convert_negated_sentence_to_negated_literal(self) -> 'Sentence':
        raise NotImplementedError("Converted negated sentences should be implemented in subclasses.")
    
    def get_cnf_subsentences(self) -> list['CNFSentence']:
        raise NotImplementedError("Getting CNF sub sentences should be implemented in subclasses.")

class AtomicSentence(Sentence):
    def __init__(self, atom: Atom):
        super().__init__()
        self.atom = atom

    def __str__(self):
        return str(self.atom)
    
    def __eq__(self, other: 'AtomicSentence'):
        return self.atom == other.atom
    
    def evaluate(self, model: Model) -> bool:
        # handle negation of the atom
        value_according_model = model.get(self.atom.name)

        # if the atom is negated, we need to negate the value according to the model
        if self.atom.negated:
            return not value_according_model
    
        return value_according_model
    
    def get_symbols(self) -> set[Literal]:
        return set([self.atom])
    
    def get_cnfs(self) -> Sentence:
        return self
    
    def convert_biconditionals(self) -> Sentence:
        return self
    
    def convert_implications(self) -> Sentence:
        return self

    def remove_double_negations(self) -> Sentence:
        return self
    
    def apply_de_morgans_laws(self) -> Sentence:
        return self
    
    def distribute_conjuctions_over_disjunctions(self) -> Sentence:
        return self
    
    def convert_negated_sentence_to_negated_literal(self) -> Sentence:
        return self
    
    def get_cnf_subsentences(self) -> list['CNFSentence']:
        return [CNFSentence(set([self.atom]))]
    
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
                    negated_sentence = Sentence.from_string(string[2:-1], known_symbols)

                    return Expression(None, Operator.NEGATION, negated_sentence)
                
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
    
    def get_cnfs(self) -> list['CNFSentence']:
        sentence = self.convert_biconditionals()

        sentence = sentence.convert_implications()

        # HUGE TODO: refactor this
        previous_string = str(sentence)
        while True:
            sentence = sentence.remove_double_negations()
            sentence = sentence.apply_de_morgans_laws()

            if previous_string == str(sentence):
                break
            previous_string = str(sentence)        

        sentence = sentence.convert_negated_sentence_to_negated_literal()

        # HUGE TODO: refactor this
        previous_string = str(sentence)
        while True:
            sentence = sentence.distribute_conjuctions_over_disjunctions()
            if previous_string == str(sentence):
                break
            previous_string = str(sentence)

        cnfs = sentence.get_cnf_subsentences()
        return cnfs
    
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
            return Expression(implication_lhs, Operator.CONJUNCTION, implication_rhs)
    
        return self

    def convert_implications(self) -> Sentence:
        # negation expression doesn't have a lhs
        if self.operator != Operator.NEGATION:
            self.lhs = self.lhs.convert_implications()
        self.rhs = self.rhs.convert_implications()

        # this isn't an infinite loop, the atomic sentence has the base case
        if self.operator == Operator.IMPLICATION:
            # split the implication using the following rule:
            # A => B === ~A || B
            not_lhs = Expression(None, Operator.NEGATION, self.lhs)
            return Expression(not_lhs, Operator.DISJUNCTION, self.rhs)
    
        return self

    def apply_de_morgans_laws(self) -> Sentence:
        # check if we are negated
        if self.operator == Operator.NEGATION:
            # if we are negated then we want to apply de morgan's laws to the rhs
            
            # if the rhs is an expression then we need to apply de morgan's laws to it
            if isinstance(self.rhs, Expression) and self.rhs.lhs is not None:
                # apply de morgan's laws to the rhs
                # NOTE: the rhs cannot be a negation because we are already removed double negations

                # get the inner expression of the negated sentence
                inner_expression = self.rhs
                inner_operator = inner_expression.operator

                # make sure that we only allow ands and ors
                if inner_operator != Operator.DISJUNCTION and inner_operator != Operator.CONJUNCTION:
                    raise ValueError("The operator is " + inner_operator.value + " and is not a disjunction or a conjunction")

                # get the lhs and rhs
                inner_lhs = inner_expression.lhs
                inner_rhs = inner_expression.rhs

                # flip the operator depending on the inner operator
                other_operator = Operator.CONJUNCTION if inner_operator == Operator.DISJUNCTION else Operator.DISJUNCTION

                # apply de morgans law
                negated_inner_lhs = Expression(None, Operator.NEGATION, inner_lhs)
                negated_inner_rhs = Expression(None, Operator.NEGATION, inner_rhs)
                return Expression(negated_inner_lhs.apply_de_morgans_laws(), other_operator, negated_inner_rhs.apply_de_morgans_laws())
            
            # if its an atom it can't be affected by de morgan's laws so we don't even need to recurse
            return self

        # apply de morgan's laws to the lhs and rhs
        self.lhs = self.lhs.apply_de_morgans_laws()
        self.rhs = self.rhs.apply_de_morgans_laws()

        return self

    def remove_double_negations(self) -> Sentence:
        # not negated so we can just recurse
        if not self.operator == Operator.NEGATION:
            self.lhs = self.lhs.remove_double_negations()
            self.rhs = self.rhs.remove_double_negations()
            return self

        # if we are negated then we need to check if the rhs is negated
        if isinstance(self.rhs, Expression):

            # rhs is negated, so its a double negation
            if self.rhs.operator == Operator.NEGATION:
                # recurse rhs
                return self.rhs.rhs.remove_double_negations()
                        
            # child is not negated so we can just recurse as there is no double negation
            self.rhs = self.rhs.remove_double_negations()
            return self
        
        # othercase is that the rhs is an atomic sentence
        self.rhs: AtomicSentence

        # if atom is negated there is a double negation
        if self.rhs.atom.negated:
            return AtomicSentence(Literal(self.rhs.atom.name, False))
        
        # not double negation
        return self

    def distribute_conjuctions_over_disjunctions(self) -> Sentence:
        # we want to distribute the disjunction over the conjunction where the conjunction is the inner expression
        if self.operator == Operator.DISJUNCTION:
            # grab the lhs and rhs
            lhs = self.lhs
            rhs = self.rhs

            # we need to distribute over the inner and outer side
            # we can't distribute over atomic sentences
            if not (isinstance(lhs, AtomicSentence) and isinstance(rhs, AtomicSentence)):

                # there are 3 other cases:
                # A || (B & C)
                # (A & B) || C
                # (A & B) || (C & D)

                # in case 3 we can choose to distribute over the lhs or rhs
                # so we just choose rhs as inner

                # so case 2 and 3 we make inner lhs
                # case 1 we make inner rhs

                if isinstance(rhs, AtomicSentence) or (isinstance(lhs, Expression) and isinstance(rhs, Expression) and rhs.operator == Operator.DISJUNCTION):
                    inner = lhs
                    outer = rhs
                else:
                    outer = lhs
                    inner = rhs
                inner: Expression
                outer: Expression
                if inner.operator == Operator.CONJUNCTION:
                    return Expression.apply_distributive_law(outer, inner)

        # recurse the distribution function to both sides of the expression
        self.lhs = self.lhs.distribute_conjuctions_over_disjunctions()
        self.rhs = self.rhs.distribute_conjuctions_over_disjunctions()

        return self
    
    @staticmethod
    def apply_distributive_law(outer: 'Sentence', inner: 'Expression') -> 'Expression':                
        distributed_lhs = Expression(outer, Operator.DISJUNCTION, inner.lhs)
        distributed_rhs = Expression(outer, Operator.DISJUNCTION, inner.rhs)
        return Expression(distributed_lhs.distribute_conjuctions_over_disjunctions(), Operator.CONJUNCTION, distributed_rhs.distribute_conjuctions_over_disjunctions())

    def convert_negated_sentence_to_negated_literal(self) -> Sentence:
        # convert to a negated atomic sentence
        if self.operator == Operator.NEGATION:
            return AtomicSentence(Literal(self.rhs.atom.name, True))
        
        # recurse
        self.lhs = self.lhs.convert_negated_sentence_to_negated_literal()
        self.rhs = self.rhs.convert_negated_sentence_to_negated_literal()
        return self

    def get_cnf_subsentences(self) -> list['CNFSentence']:
        # (~a || ~b) || ((d || c) & (d || f))
        # (~a || ~b) || ((d || c) & (d || f))
        # (~a || ~b || d || c) & (d || f)
        sentence_string = str(self).replace(" ", "").replace(Operator.OPENING_BRACKET.value, "").replace(Operator.CLOSING_BRACKET.value, "")
        disjunction_sentences = sentence_string.split(Operator.CONJUNCTION.value)

        cnfs = []
        for disjunction_sentence in disjunction_sentences:
            literals_as_strings = disjunction_sentence.split(Operator.DISJUNCTION.value)

            literals = [Literal.from_string(literal_string) for literal_string in literals_as_strings]
                
            cnfs.append(CNFSentence(set(literals)))

        return cnfs

# Horn Clause implication form is always A & B & C => D with all positive literals, there cannot be any negative literals
# more info: https://stackoverflow.com/questions/45123756/why-do-we-call-a-disjunction-of-literals-of-which-none-is-positive-a-goal-clause

class HornClause(Expression):
    def __init__(self, body: list[PositiveLiteral], head: PositiveLiteral, known_symbols: set[Literal]):
        self.body = body
        self.head = head

        lhs = Sentence.from_string(Operator.CONJUNCTION.value.join([str(literal) for literal in self.body]), known_symbols)
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
    
class CNFSentence:
    def __init__(self, disjunction_literals: set[Literal]):
        sorted_disjunctions = sorted(list(disjunction_literals))

        self.disjunction_literals = disjunction_literals

        sentence_string = Operator.DISJUNCTION.value.join([str(literal) for literal in sorted_disjunctions])

        self.sentence = Sentence.from_string(sentence_string, set())

        # local model
        self.model = Model({symbol.name: None for symbol in sorted_disjunctions})


    def is_tautology(self) -> bool:
        for symbol in self.disjunction_literals:
            if Literal(symbol.name, not symbol.negated) in self.disjunction_literals:
                return True
        return False
    
    def __str__(self):
        return str(self.sentence)