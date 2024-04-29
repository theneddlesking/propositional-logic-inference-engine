from src.inference_algorithm import InferenceAlgorithm

class ForwardChaining(InferenceAlgorithm):
    def __init__(self):
        super().__init__("FC")