

class TestCase:
    _case_id = 1

    def __init__(self, module: str, summary: str, steps: list[str], expected_results: list[str]):
        self._module = self.format_content(module)
        self._summary = self.format_content(summary)
        self._steps = [self.format_content(step) for step in steps]
        self._expected_results = [self.format_content(expected_result) for expected_result in expected_results]
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
        self._precondition = self.format_content(precondition)

    def __str__(self):
        return f"({self.case_id}) 【{self.module}】{self.summary}"

    # 处理文字中存在"符合导致转化成csv时格式，错乱，在有""的内容上再嵌套一层"",
    # 如： "testcases" 转化成 ""testcases""
    @staticmethod
    def format_content(content : str):
        new_content = ""
        for s in content:
            if s == '"':
                new_content += '"'
            new_content += s
        return new_content


