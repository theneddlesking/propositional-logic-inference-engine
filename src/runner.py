from src.algorithm_result import AlgorithmResult
from src.cnf_knowledge_base import CNFKnowledgeBase
from src.file_parser import FileParser, FileType
from src.horn_knowledge_base import HornKnowledgeBase
from src.inference_algorithm import InferenceAlgorithm
from src.query import HornKnowledgeBaseQuery
from src.test.unit_test_result import UnitTestResult

class Runner:
    
    @staticmethod
    def run_from_file_path(algorithm: InferenceAlgorithm, file_path: str) -> AlgorithmResult:
        # get the knowledge base and query from the file
        knowledge_base, query = FileParser.parse_kb_and_query(file_path)

        # only works on horn kb so we make some conversions
        if algorithm.name == "FC" or algorithm.name == "BC":

            # convert to horn kb if algorithm is FC or BC
            knowledge_base = HornKnowledgeBase.from_generic_knowledge_base(knowledge_base)

            # convert to horn query if algorithm is FC or BC
            positive_literal = query.sentence.atom

            query = HornKnowledgeBaseQuery(positive_literal)
        elif algorithm.name == 'DPLL':
            # convert to cnf kb
            print("KB:")
            print("Before")
            print(knowledge_base)
            knowledge_base = CNFKnowledgeBase.from_generic_knowledge_base(knowledge_base)
            print("After")
            print(knowledge_base)

        # run the algorithm
        return algorithm.run(knowledge_base, query)
                
    @staticmethod
    def run_test_from_file_path(algorithm: InferenceAlgorithm, file_path: str) -> UnitTestResult:
        # validate the file is correct
        file_type = FileParser.get_file_type(file_path)

        # check that it is a test file
        if file_type != FileType.CHAINING_TEST and file_type != FileType.TRUTH_TABLE_CHECKING_TEST:
            raise ValueError("File is not a test file")

        # TODO: refactor duplicate code
        # get the knowledge base and query from the file
        knowledge_base, query = FileParser.parse_kb_and_query(file_path)

        # only works on horn kb so we make some conversions
        if algorithm.name == "FC" or algorithm.name == "BC":

            # convert to horn kb if algorithm is FC or BC
            knowledge_base = HornKnowledgeBase.from_generic_knowledge_base(knowledge_base)

            # convert to horn query if algorithm is FC or BC
            positive_literal = query.sentence.atom

            query = HornKnowledgeBaseQuery(positive_literal)

        # get the expected result
        expected_result, name, description = FileParser.parse_test(file_path, file_type, algorithm.name)

        # get the actual result
        actual_result = algorithm.run(knowledge_base, query)

        # compare the results by building the test case
        test = UnitTestResult(name, description, algorithm.name, knowledge_base, query, expected_result, actual_result)

        # return the test result
        return test
