# Class for the truth table algorithm result
# You can think of it as the row of a typical truth table
# where all the literals are assigned either true or false
class Model():
    def __init__(self, values: list[dict[str, bool]]):
        self.values = values

    def __str__(self) -> str:
        str = ""

        for key, value in self.values.items():
            str += f"{key}: {value} | "

        # remove the last " | "
        str = str[:-3]

        return str
    
    def get(self, symbol: str) -> bool:
        return self.values[symbol]