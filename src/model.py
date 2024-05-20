# Class for the truth table algorithm result
# You can think of it as the row of a typical truth table
# where all the literals are assigned either true or false
class Model():
    def __init__(self, values: dict[str, bool]):
        # sort the keys alphabetically
        values = dict(sorted(values.items()))        

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
    
    def __eq__(self, other: 'Model') -> bool:
        return self.values == other.values
    
    def __lt__(self, other: 'Model') -> bool:
        return str(self) < str(other)