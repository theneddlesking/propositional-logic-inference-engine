# entry point for the program

import sys

from src.inference_algorithm_factory import InferenceAlgorithmFactory
from src.runner import Runner


def main():
    # not enough arguments
    if len(sys.argv) < 3:
        print(
            "Usage: python iengine.py <file_path> <inference_algorithm> [--test / --debug]"
        )
        return

    # get the file name and inference algorithm name
    file_path = sys.argv[1]
    inference_algorithm_name = sys.argv[2].upper()

    # test mode
    is_test_file = ("--test" in sys.argv) if len(sys.argv) > 3 else False

    # debug mode
    debug = ("--debug" in sys.argv) if len(sys.argv) > 3 else False

    # get the inference algorithm
    inference_algorithm = InferenceAlgorithmFactory.get_inference_algorithm_from_name(
        inference_algorithm_name
    )

    if is_test_file:
        # run the test
        result = Runner.run_test_from_file_path(inference_algorithm, file_path)

        # print the result in green if passed, red if failed

        if result.passed:
            print(f"\033[92m{result}\033[0m")
        else:
            print(f"\033[91m{result}\033[0m")

        return

    # run the algorithm
    result = Runner.run_from_file_path(inference_algorithm, file_path)

    if debug:
        # print the result in debug mode
        print(result.debug())
        return

    # print the result
    print(result)


# runs the program if the file is run directly
if __name__ == "__main__":
    main()
