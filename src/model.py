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
    
    def set_value(self, symbol: str, value: bool, negated: False = bool):
        # only add it if it exists in the model
        if symbol in self.values:
            if not negated:
                self.values[symbol] = value
            else:
                self.values[symbol] = not value
    
    def get(self, symbol: str) -> bool:
        return self.values[symbol]
    
    def copy(self) -> 'Model':
        return Model(self.values.copy())
    
    def __eq__(self, other: 'Model') -> bool:
        return self.values == other.values
    
    def __lt__(self, other: 'Model') -> bool:
        return str(self) < str(other)