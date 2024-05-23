from src.cnf_knowledge_base import CNFKnowledgeBase
from src.inference_algorithm import InferenceAlgorithm
from src.model import Model
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

        # symbols
        symbols = knowledge_base.symbols

        # if query symbol not in knowledge base then it must be unsatisfiable
        for clause in query_cnfs:
            for literal in clause.literals:
                if literal.name not in symbols:
                    return DPLLResult(False, knowledge_base.copy())
                
        # all symbols start unassigned
        model = Model({symbol: None for symbol in symbols})

        # run dpll
        satisfiable = self.dpll(knowledge_base, model)

        return DPLLResult(satisfiable, knowledge_base.copy())        

    def dpll(self, cnf: CNFKnowledgeBase, model: Model) -> bool:
        # cnf satisfied
        if cnf.satisfies(model):
            return True
        
        # cnf contains empty clause and therefore is unsatisfiable
        if cnf.contains_empty_clause():
            return False
        
        # choose a symbol that is not yet assigned
        symbol = self.choose_symbol(model)

        # no more symbols to assign, check if the cnf is satisfied
        if symbol is None:
            return False

        # create positive and negative models
        positive_model = model.copy()
        positive_model.set(symbol.name, True)

        negative_model = model.copy()
        negative_model.set(symbol.name, False)

        # simplify the cnf
        simplified_cnf_positive = cnf.simplify(positive_model)
        simplified_cnf_negative = cnf.simplify(negative_model)

        # recursively call dpll
        return self.dpll(simplified_cnf_positive, positive_model) or self.dpll(simplified_cnf_negative, negative_model)

    
    def choose_symbol(self, model: Model) -> Literal:
        for symbol, value in model.values.items():
            if value is None:
                return Literal(symbol)
        return None
