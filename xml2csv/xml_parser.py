from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from testcase import TestCase


class XMLParser:

    def __init__(self, file_path: str):
        tree = ET.parse(file_path)
        self._root = tree.getroot()

    def parse_xml(self):
        testcases_collection = []
        for module, summary in self._case_gen():
            dept = self.get_depth(summary)
            expected_results = []
            steps = []
            # have precondition node
            if dept > 3:
                for precondition in summary:
                    for step in precondition:
                        steps.append(step.get("TEXT"))
                        for expected_result in step:
                            expected_results.append(expected_result.get("TEXT"))
                    testcase = TestCase(module.get("TEXT"), summary.get("TEXT"), steps, expected_results)
                    testcase.precondition = precondition.get("TEXT")
                    testcases_collection.append(testcase)
            else:
                for step in summary:
                    steps.append(step.get("TEXT"))
                    for expected_result in step:
                        expected_results.append(expected_result.get("TEXT"))
                testcase = TestCase(module.get("TEXT"), summary.get("TEXT"), steps, expected_results)
                testcases_collection.append(testcase)

        return testcases_collection

    def _theme_gen(self):
        for theme in self._root:
            if theme.tag == "node":
                yield theme

    def _module_gen(self):
        for theme in self._theme_gen():
            yield from (module for module in theme if module.tag == "node")

    def _case_gen(self):
        for module in self._module_gen():
            yield from ((module, case) for case in module if case.tag == "node")

    @staticmethod
    def get_depth(e: Element):
        depth = 1
        while len(e) > 0:
            depth += 1
            for child in e:
                if child.tag == "node":
                    e = child
                    break
        return depth


if __name__ == '__main__':
    a = XMLParser("E:\document\mac_doc\webull_testcases\hcm_employee_testcases.mm")
    res = a.parse_xml()
    for i in res:
        print(i)