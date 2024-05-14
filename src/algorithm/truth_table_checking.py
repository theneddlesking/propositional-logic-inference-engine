from src.inference_algorithm import InferenceAlgorithm
from src.knowledge_base import KnowledgeBase
from src.model import Model
from src.query import Query
from src.result.chaining_result import ChainingResult
from src.result.truth_table_checking_result import TruthTableCheckingResult
from src.syntax.literal import Literal

class TruthTableChecking(InferenceAlgorithm):
    def __init__(self):
        super().__init__("TT")

    def run(self, knowledge_base: KnowledgeBase, query: Query) -> ChainingResult:
        # sentence of the query to check
        query_sentence = query.sentence

        # get all the symbols in the kb
        symbols = list(knowledge_base.propositional_symbols.values())

        # get all known facts which we don't need to check again
        facts = knowledge_base.get_fact_literals()

        # get all the symbols that we need to check which aren't in the facts
        unknown_symbols = [symbol for symbol in symbols if symbol not in facts]

        # find all possible models regardless of whether they are valid or not
        unvalidated_models = self.find_all_models(unknown_symbols, facts)

        # add the query sentence to the knowledge base to verify the models
        all_sentences = knowledge_base.sentences + [query_sentence]

        # get the valid models, where all sentences are true
        valid_models = [model for model in unvalidated_models if all([sentence.evaluate(model) for sentence in all_sentences])]
    
        # if there are any valid models then the query is true
        found = len(valid_models) > 0

        return TruthTableCheckingResult(valid_models, found)


    def find_all_models(self, unknown: list[Literal], known: list[Literal]) -> list[Model]:
        # get all permutations of the unknown symbols
        permutations = self.get_permutations(unknown)

        # convert known list to dict
        known_dict = {symbol: not symbol.negated for symbol in known}

        def merge_dicts(dict1: dict, dict2: dict) -> dict:
            merged = dict1.copy()  
            merged.update(dict2)
            return merged

        # create a model for each permutation
        models = [Model(merge_dicts(known_dict, permutation)) for permutation in permutations]

        return models

    def get_permutations(self, unknown: list[Literal]) -> list[dict[Literal, bool]]:
        # get the number of unknown symbols
        n = len(unknown)

        # get the number of permutations
        num_permutations = 2**n

        # get all permutations
        permutations = [self.get_permutation(i, unknown) for i in range(num_permutations)]

        return permutations
    
    def get_permutation(self, i: int, unknown: list[Literal]) -> dict[Literal, bool]:
        # get the binary representation of the number, skip first two characters "0b" eg. "0b1001" -> "1001"
        binary = bin(i)[2:]

        # pad the binary number with 0s
        binary = binary.zfill(len(unknown))

        # create the permutation converting the binary string to a dict
        # eg. "1001" and ["A", "B", "C", "D"] -> {"A": True, "B": False, "C": False, "D": True}
        permutation = {symbol: value == "1" for symbol, value in zip(unknown, binary)}

        return permutation
    