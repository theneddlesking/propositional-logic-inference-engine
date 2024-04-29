from src.inference_algorithm import InferenceAlgorithm

class BackwardChaining(InferenceAlgorithm):
    def __init__(self):
        super().__init__("BC")