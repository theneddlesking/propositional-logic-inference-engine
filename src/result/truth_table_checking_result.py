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

        self.print_truth_table()
        
        return f"{found}: {number_of_models}"

    def print_truth_table(self):
        # get all the symbols
        if len(self.models) == 0:
            print("There were no suitable models found to print the table")
            return

        symbols: list[str] = list(self.models[0].values.keys())

        # order alphabetically
        symbols.sort()

        # determine the maximum width needed for each column
        # minimum of 6 for false ("False " requires 6 characters)
        col_width = max(6, max(len(symbol) for symbol in symbols))

        # print the symbols with adjusted width
        for symbol in symbols:
            print(f"{symbol: <{col_width}}", end="| ")

        print()

        # print the values with adjusted width
        for model in self.models:
            for symbol in symbols:
                value = model.get(symbol)
                value_str = str(value)
                print(f"{value_str: <{col_width}}", end="| ")
            print()

    def __eq__(self, other: 'TruthTableCheckingResult') -> bool: 
        return self.found == other.found and self.models == other.models