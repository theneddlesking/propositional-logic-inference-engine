import os
import sys

from src.file_parser import FileParser, FileType
from src.inference_algorithm_factory import InferenceAlgorithmFactory
from src.runner import Runner
from src.test.unit_test_result import UnitTestResult


def main():
    # not enough arguments
    if len(sys.argv) < 2:
        print("Usage: python test.py <test_folder_path> [<algorithm type?>]")
        return

    # get the folder name
    test_folder_path = sys.argv[1]

    overall_results: list[UnitTestResult] = []

    # failed tests
    failed_tests: list[str] = []

    # get algorithm type if it exists
    algorithm_type = sys.argv[2] if len(sys.argv) > 2 else None

    test_number = 1

    # for each file in the folder
    for file in os.listdir(test_folder_path):
        # get the file path
        file_path = os.path.join(test_folder_path, file)

        # get file type
        file_type = FileParser.get_file_type(file_path)

        if file_type == FileType.STANDARD:
            raise ValueError(
                f"All files should be test files. {file} is not a test file"
            )

        # get the inference algorithms
        inference_algorithms = (
            InferenceAlgorithmFactory.get_inference_algorithms_from_file_type(file_type)
        )

        # if we have specified a specifc algorithm and it's not in the list we can't do it for this file
        if algorithm_type and algorithm_type not in [
            algorithm.name for algorithm in inference_algorithms
        ]:
            continue

        # otherwise set the inference algorithms to the one specified
        if algorithm_type:
            inference_algorithms = [
                InferenceAlgorithmFactory.get_inference_algorithm_from_name(
                    algorithm_type
                )
            ]

        # for each algorithm
        for algorithm in inference_algorithms:
            # print the test number
            print(f"Test #{test_number} " + "-" * 50 + "\n")

            # run the test
            result = Runner.run_test_from_file_path(algorithm, file_path)

            # print the result in green if passed, red if failed
            if result.passed:
                print(f"\033[92m{result}\033[0m")
            else:
                print(f"\033[91m{result}\033[0m")
                failed_tests.append(f"#{test_number}")

            overall_results.append(result)

            test_number += 1

    # print the overall results
    print("Overall Results:")

    # number passed
    number_passed = len([result for result in overall_results if result.passed])

    # all passed
    if all(result.passed for result in overall_results):
        # as fraction
        print(
            f"\033[92mAll tests passed ({number_passed}/{len(overall_results)})\033[0m"
        )

    else:
        # as fraction
        print(f"\033[91m{number_passed}/{len(overall_results)} tests passed\033[0m")

        # print failed test numbers
        failed_tests_str = ", ".join([str(test) for test in failed_tests])
        print(f"Failed Tests: {failed_tests_str}")


# runs the program if the file is run directly
if __name__ == "__main__":
    main()
