from src.cnf_knowledge_base import CNFKnowledgeBase
from src.inference_algorithm import InferenceAlgorithm
from src.query import Query
from src.result.dpll_result import DPLLResult
from src.syntax.literal import Literal


class DPLL(InferenceAlgorithm):

    def __init__(self):
        super().__init__("DPLL")

    def run(self, knowledge_base: CNFKnowledgeBase, query: Query) -> DPLLResult:
        # convert query cnf
        query_cnfs = query.sentence.get_cnfs()

        # add cnfs
        knowledge_base.clauses.extend(query_cnfs)

        satisifable = self.dpll(knowledge_base)

        return DPLLResult(satisifable, knowledge_base.copy())        

    def dpll(self, cnf: CNFKnowledgeBase) -> bool:
        # the clause is a unit clause if it has only one unassigned literal and the rest are false
        # the one unassigned literal is the unit literal

        # a clause is true if for each literal in the clause, the literal is true (satisfies the partial model)
        # otherwise the clause is unassigned

        # a formula is true if all clauses in the formula are true
        # a formula is false if one clause in the formula is false
        # otherwise the formula is unassigned

        # propogate unit literals from unit clauses
        while cnf.has_unit_clause():
            # propagate the unit literal
            cnf.unit_propagate()

        pure_literals = cnf.get_pure_literals()

        # check for pure symbols
        # pure symbols are symbols that only appear as positive or negative literals throughout the knowledge base
        for literal in pure_literals:
            cnf.assign_pure_literal(literal)

        if cnf.is_empty():
            return True
        
        if cnf.has_empty_clause():
            return False
        
        # choose a symbol
        p = cnf.choose_symbol()

        # create a new knowledge base with p assigned true
        knowledge_base_true = cnf.copy()

        knowledge_base_true.assign(p, True)

        # create a new knowledge base with p assigned false
        knowledge_base_false = cnf.copy()

        knowledge_base_false.assign(p, False)

        return self.dpll(knowledge_base_true) or self.dpll(knowledge_base_false)
    
