from src.syntax.literal import Literal

# Class for the truth table algorithm result
# You can think of it as the row of a typical truth table
# where all the literals are assigned either true or false
class Model():
    def __init__(self, values: list[dict[Literal, bool]]):
        self.values = values