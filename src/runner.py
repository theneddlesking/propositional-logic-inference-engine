from src.algorithm_result import AlgorithmResult
from src.file_parser import FileParser
from src.horn_knowledge_base import HornKnowledgeBase
from src.inference_algorithm import InferenceAlgorithm
from src.query import HornKnowledgeBaseQuery

class Runner:
    
    @staticmethod
    def run_from_file_path(algorithm: InferenceAlgorithm, file_path: str) -> AlgorithmResult:
        # get the knowledge base and query from the file
        knowledge_base, query = FileParser.parse_standard_file_from_path(file_path)

        # only works on horn kb so we make some conversions
        if algorithm.name == "FC" or algorithm.name == "BC":

            # convert to horn kb if algorithm is FC or BC
            knowledge_base = HornKnowledgeBase.from_generic_knowledge_base(knowledge_base)

            # convert to horn query if algorithm is FC or BC
            positive_literal = query.sentence.atom

            query = HornKnowledgeBaseQuery(positive_literal)

        print(knowledge_base)
        
        # run the algorithm
        return algorithm.run(knowledge_base, query)