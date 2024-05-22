from src.model import Model
from src.syntax.literal import Literal


class CNFModel(Model):
    def __init__(self, values: dict[Literal, bool]):
        # sort the keys alphabetically
        values = dict(sorted(values.items()))

        self.values = values
    
    def set_value(self, literal: Literal, value: bool):
        # only add it if it exists in the model
        if literal in self.values:
            if literal.negated:
                self.values[literal] = not value
            else:
                self.values[literal] = value
    
    def get(self, literal: Literal) -> bool:
        return self.values[literal]
    
    def copy(self) -> 'CNFModel':
        return CNFModel(self.values.copy())
    
    def __eq__(self, other: 'CNFModel') -> bool:
        return self.values == other.values
    
    def __lt__(self, other: 'CNFModel') -> bool:
        return str(self) < str(other)