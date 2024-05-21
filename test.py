import os
import sys

from src.file_parser import FileParser, FileType
from src.inference_algorithm_factory import InferenceAlgorithmFactory
from src.runner import Runner
from src.test.unit_test_result import UnitTestResult

def main():
    # not enough arguments
    if len(sys.argv) < 2:
        print("Usage: python test.py <test_folder_path>")
        return

    # get the folder name
    test_folder_path = sys.argv[1]

    overall_results: list[UnitTestResult] = []

    # for each file in the folder
    for file in os.listdir(test_folder_path):
        # get the file path
        file_path = os.path.join(test_folder_path, file)

        # get file type
        file_type = FileParser.get_file_type(file_path)

        if file_type == FileType.STANDARD:
            raise ValueError(f"All files should be test files. {file} is not a test file")

        # get the inference algorithms
        inference_algorithms = InferenceAlgorithmFactory.get_inference_algorithms_from_file_type(file_type)

        # for each algorithm
        for algorithm in inference_algorithms:
            # run the test
            result = Runner.run_test_from_file_path(algorithm, file_path)

            # print the result in green if passed, red if failed
            if result.passed:
                print(f"\033[92m{result}\033[0m")
            else:
                print(f"\033[91m{result}\033[0m")

            overall_results.append(result)

    # print the overall results
    print("Overall Results:")

    # number passed
    number_passed = len([result for result in overall_results if result.passed])

    # all passed
    if all(result.passed for result in overall_results):
        # as fraction
        print(f"\033[92mAll tests passed ({number_passed}/{len(overall_results)})\033[0m")
    else:
        # as fraction
        print(f"\033[91m{number_passed}/{len(overall_results)} tests passed\033[0m")

    
    



# runs the program if the file is run directly
if __name__ == '__main__':
    main()