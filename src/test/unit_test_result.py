class UnitTestResult:
    def __init__(self, name: str, description: str, expect, actual):
        self.name = name
        self.description = description
        self.expect = expect
        self.actual = actual

        self.passed = expect == actual

    def __str__(self):
        passed_str = "PASSED" if self.passed else "FAILED"
        return f"{self.name} - {passed_str}\n{self.description}\nExpected: {self.expect.debug()}\nActual: {self.actual.debug()}\n"
    