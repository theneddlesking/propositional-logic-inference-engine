from src.knowledge_base import KnowledgeBase
from src.syntax.literal import Literal
from src.syntax.sentence import CNFClause, Sentence

class CNFKnowledgeBase(KnowledgeBase):

    def __init__(self, propositional_symbols: set[Literal], cnf_sentences: list[CNFClause]):
        self.clauses = cnf_sentences

        self.unit_literal_to_propogate = None

        super().__init__(cnf_sentences, propositional_symbols)

    @classmethod
    def from_generic_knowledge_base(cls, knowledge_base: KnowledgeBase):
        # get the cnf version of all the sentences
        cnf_sentences: list[CNFClause] = []

        for sentence in knowledge_base.sentences:
            res = sentence.get_cnfs()
            cnf_sentences.extend(sentence.get_cnfs())

        # filter out invalid sentences
        valid_cnf_sentences = [sentence for sentence in cnf_sentences if not sentence.is_tautology()]

        return cls(knowledge_base.propositional_symbols, valid_cnf_sentences)
    
    def has_unit_clause(self) -> bool:
        for clause in self.clauses:
            if clause.is_unit_clause():
                self.unit_literal_to_propogate = clause.get_unit_literal()
                return True
        return False
    
    def is_empty(self) -> bool:
        return all([clause.is_empty() for clause in self.clauses])
    
    def has_empty_clause(self) -> bool:
        return any([clause.is_empty() for clause in self.clauses])
    
    def unit_propagate(self):
        # each sentence needs to be updated
        for clause in self.clauses:
            clause.update_model(self.unit_literal_to_propogate, clause.find_literal_negation(self.unit_literal_to_propogate.name))

        # set the unit literal to None
        self.unit_literal_to_propogate = None

    def get_pure_literals(self) -> set[Literal]:
        # get all the literals
        literals = [literal for clause in self.clauses for literal in clause.disjunction_literals]

        # positive literals
        positive_literal_symbols = [literal.name for literal in literals if not literal.negated]

        # negative literals
        negative_literals_symbols = [literal.name for literal in literals if literal.negated]

        # find the difference
        positive_symbols = set(positive_literal_symbols) - set(negative_literals_symbols)
        negative_symbols = set(negative_literals_symbols) - set(positive_literal_symbols)

        # get the pure symbols
        pure_symbols = set(positive_symbols) | set(negative_symbols)

        # get the pure literals
        pure_literals = set([(Literal(symbol_name, symbol_name in negative_symbols)) for symbol_name in pure_symbols])
        
        return pure_literals
    
    def assign_pure_literal(self, pure_literal: Literal):
        for clause in self.clauses:
            clause.update_model(pure_literal, clause.find_literal_negation(pure_literal.name))

    def choose_symbol(self) -> Literal:
        for clause in self.clauses:
            model = clause.model
            for symbol, state in model.values.items():
                if state is None:
                    return symbol
        raise ValueError("All symbols have a value assigned")
    
    def assign(self, symbol: str, state: bool):
        for clause in self.clauses:
            clause.update_model(Literal(symbol, not state), clause.find_literal_negation(symbol))
    
    def copy(self) -> 'CNFKnowledgeBase':
        new_sentences = [clause.copy() for clause in self.clauses]
        return CNFKnowledgeBase(self.propositional_symbols, new_sentences)
  