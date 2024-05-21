class UnitTestResult:
    def __init__(self, name: str, description: str, algorithm_name: str, expect, actual):
        self.name = name
        self.description = description

        self.algorithm_name = algorithm_name

        self.expect = expect
        self.actual = actual


        self.passed = expect == actual

    def __str__(self):
        passed_str = "PASSED" if self.passed else "FAILED"
        return f"{self.name} ({self.algorithm_name}) - {passed_str}\n{self.description}\nExpected: {self.expect.debug()}\nActual: {self.actual.debug()}\n"
    