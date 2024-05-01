# entry point for the program

import sys

from src.inference_algorithm_factory import InferenceAlgorithmFactory
from src.runner import Runner

def main():
    # not enough arguments
    if len(sys.argv) < 3:
        print("Usage: python iengine.py <file_path> <inference_algorithm>")
        return

    # get the file name and inference algorithm name
    file_path = sys.argv[1]
    inference_algorithm_name = sys.argv[2].upper()

    # get the inference algorithm
    inference_algorithm = InferenceAlgorithmFactory.get_inference_algorithm_from_name(inference_algorithm_name)

    # run the algorithm
    result = Runner.run_from_file_path(inference_algorithm, file_path)

    # print the result
    print(result)

# runs the program if the file is run directly
if __name__ == '__main__':
    main()