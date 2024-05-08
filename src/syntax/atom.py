class Atom:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name
    
class BoolAtom(Atom):
    def __init__(self, bool: bool):
        name = "True" if bool else "False"
        super().__init__(name, bool)

    @classmethod
    def from_string(cls, string: str) -> 'BoolAtom':
        # needs to be True or False
        if string != "True" and string != "False":
            raise ValueError(f"{string} is not a valid boolean value. Should be True or False.")

        return cls(string == "True")