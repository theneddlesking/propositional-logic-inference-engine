from src.algorithm_result import AlgorithmResult
from src.file_parser import FileParser
from src.inference_algorithm import InferenceAlgorithm

class Runner:
    
    @staticmethod
    def run_from_file_path(algorithm: InferenceAlgorithm, file_path: str) -> AlgorithmResult:
        # get the knowledge base and query from the file
        knowledge_base, query = FileParser.parse_standard_file_from_path(file_path)
        
        # run the algorithm
        return algorithm.run(knowledge_base, query)