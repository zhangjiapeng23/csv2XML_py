

class TestCase:
    _case_id = 1

    def __init__(self, module: str, summary: str, steps: list[str], expected_results: list[str]):
        self._module = module
        self._summary = summary
        self._steps = steps[:]
        self._expected_results = expected_results[:]
        self._case_id = self.__class__._case_id
        self.__class__._case_id += 1
        self._precondition = None

    @property
    def case_id(self):
        return self._case_id

    @property
    def module(self):
        return self._module

    @property
    def summary(self):
        return self._summary

    @property
    def steps(self):
        return self._steps

    @property
    def expected_results(self):
        return self._expected_results

    @property
    def precondition(self):
        return self._precondition

    @precondition.setter
    def precondition(self, precondition):
        self._precondition = precondition

    def __str__(self):
        return f"({self.case_id}) 【{self.module}】{self.summary}"


if __name__ == '__main__':
    case1 = TestCase("1", "1", [], [])
    case2 = TestCase("2", "2", [], [])
    print(case1)
    print(case2)
