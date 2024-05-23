from src.cnf_clause import CNFClause
from src.knowledge_base import KnowledgeBase
from src.model import Model
from src.syntax.literal import Literal

class CNFKnowledgeBase():

    def __init__(self, cnf_clauses: list[CNFClause], symbols: set[str] = set()):
        self.clauses = cnf_clauses
        self.symbols = symbols

    @classmethod
    def from_generic_knowledge_base(cls, knowledge_base: KnowledgeBase):
        # get the cnf version of all the sentences
        cnf_clauses: list[CNFClause] = []

        for sentence in knowledge_base.sentences:
            cnf_clauses.extend(sentence.get_cnfs())

        # filter out invalid sentences
        valid_clauses = [clause for clause in cnf_clauses if not clause.is_tautology()]

        # filter out duplicate sentences
        string_valid_clauses = list(set([str(clause) for clause in valid_clauses]))
        valid_clauses: list[CNFClause] = [CNFClause.from_string(clause) for clause in string_valid_clauses]

        # all symbols
        symbols = set()

        for clause in valid_clauses:
            for literal in clause.literals:
                symbols.add(literal.name)

        return cls(valid_clauses, symbols)
    
    def copy(self) -> 'CNFKnowledgeBase':
        return CNFKnowledgeBase([clause.copy() for clause in self.clauses], self.symbols.copy())
  
    def satisfies(self, model: Model) -> bool:
        return all(clause.satisfies(model) for clause in self.clauses)
    
    def contains_empty_clause(self) -> bool:
        return any(clause.is_empty() for clause in self.clauses)
    
    def simplify(self, model: Model) -> 'CNFKnowledgeBase':
        new_clauses: list[CNFClause] = []

        # only keep the clauses that are not satisfied
        unsatisied_clauses: list[CNFClause] = [clause for clause in self.clauses if not clause.satisfies(model)]

        # simplify the unsatisfied clauses
        new_clauses = [clause.simplify(model) for clause in unsatisied_clauses]

        return CNFKnowledgeBase(new_clauses, self.symbols)

