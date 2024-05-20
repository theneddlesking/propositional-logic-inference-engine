class TestCase:
    def __init__(self, name: str, expect, actual):
        self.name = name
        self.expect = expect
        self.actual = actual

        self.passed = expect == actual

    def __str__(self):
        return f"{self.name}: {self.expect} == {self.actual}"
    
    def __repr__(self):
        return self.__str__()