from src.algorithm_result import AlgorithmResult
from src.model import Model
from src.syntax.literal import Literal

class TruthTableCheckingResult(AlgorithmResult):
    def __init__(self, models: list[Model], found: bool):
        super().__init__("TT")
        self.found = found

        # sort
        models.sort()

        self.models = models


    def __str__(self) -> str:
        # yes or no
        found = "YES" if self.found else "NO"

        number_of_models = len(self.models)
        
        return f"{found}: {number_of_models}"

    def get_truth_table_str(self):
        string = ""

        # get all the symbols
        if len(self.models) == 0:
            string += "There were no suitable models found to print the table"
            return string

        symbols: list[str] = list(self.models[0].values.keys())

        # order alphabetically
        symbols.sort()

        # determine the maximum width needed for each column
        # minimum of 6 for false ("False " requires 6 characters)
        col_width = max(6, max(len(symbol) for symbol in symbols))

        # print the symbols with adjusted width
        for symbol in symbols:
            string += f"{symbol: <{col_width}}| "

        string += "\n"

        # print the values with adjusted width
        for model in self.models:
            for symbol in symbols:
                value = model.get(symbol)
                value_str = str(value)
                string += f"{value_str: <{col_width}}| "
            string += "\n"

        # remove the last newline
        string = string[:-1]
        
        return string

    def __eq__(self, other: 'TruthTableCheckingResult') -> bool: 
        return self.found == other.found and self.models == other.models
    
    def debug(self):
        str = super().debug()
        str += "\n"
        # add table
        str += self.get_truth_table_str()
        return str