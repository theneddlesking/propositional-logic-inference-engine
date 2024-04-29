from src.file_parser import FileParser
from src.inference_algorithm import InferenceAlgorithm

class Runner:
    def __init__(self):
        pass

    def run_from_file_path(self, algorithm: InferenceAlgorithm, file_path: str):
        # get the knowledge base and query from the file
        knowledge_base, query = FileParser.parse_standard_file_from_path(file_path)

        # TODO create a proper return object for the run method
        
        # run the algorithm
        return algorithm.run(knowledge_base, query)