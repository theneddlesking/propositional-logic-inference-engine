from src.syntax.literal import Literal

# Class for the truth table algorithm result
# You can think of it as the row of a typical truth table
# where all the literals are assigned either true or false
class Model():
    def __init__(self, values: list[dict[Literal, bool]]):
        self.values = values

    def __str__(self) -> str:
        str = ""

        for key, value in self.values.items():
            str += f"{key}: {value} | "

        # remove the last " | "
        str = str[:-3]

        return str
    
    def get(self, symbol: Literal) -> bool:
        return self.values[symbol]