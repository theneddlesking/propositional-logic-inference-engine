from src.algorithm.backward_chaining import BackwardChaining
from src.algorithm.dpll import DPLL
from src.algorithm.forward_chaining import ForwardChaining
from src.algorithm.test_algorithm import TestAlgorithm
from src.algorithm.truth_table_checking import TruthTableChecking
from src.file_parser import FileType
from src.inference_algorithm import InferenceAlgorithm


class InferenceAlgorithmFactory:

    # gets the list of all implemented inference algorithms
    @staticmethod
    def get_inference_algorithms():
        algorithms: list[InferenceAlgorithm] = [
            TruthTableChecking(),
            ForwardChaining(),
            BackwardChaining(),
            DPLL(),
            TestAlgorithm(),
        ]
        return algorithms

    @staticmethod
    def get_inference_algorithm_from_name(name: str):
        # get known algorithms
        algorithms = InferenceAlgorithmFactory.get_inference_algorithms()

        # check all algorithms to see if we can find the one with the given name
        for algorithm in algorithms:
            if algorithm.name == name:
                return algorithm

        # we couldn't find the algorithm

        # get list of names of all valid algorithms to show in error message
        names = [algorithm.name for algorithm in algorithms]

        # throw the error
        raise ValueError(
            f"Algorithm with name {name} not found, Valid algorithms are: {names}"
        )

    @staticmethod
    def get_inference_algorithms_from_file_type(
        file_type: FileType,
    ) -> list[InferenceAlgorithm]:
        # filter the algorithms based on the file type
        if file_type == FileType.TRUTH_TABLE_CHECKING_TEST:
            return [
                InferenceAlgorithmFactory.get_inference_algorithm_from_name("TT"),
                InferenceAlgorithmFactory.get_inference_algorithm_from_name("DPLL"),
            ]
        elif file_type == FileType.CHAINING_TEST:
            return [
                InferenceAlgorithmFactory.get_inference_algorithm_from_name("FC"),
                InferenceAlgorithmFactory.get_inference_algorithm_from_name("BC"),
            ]

        raise ValueError("Invalid file type")
