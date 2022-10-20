from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from xml2csv.testcase import TestCase


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
                    if precondition.tag != "node":
                        continue
                    for step in precondition:
                        if step.tag != "node":
                            continue
                        # steps.append(step.get("TEXT"))
                        steps.append(self._parse_node_text(step))
                        for expected_result in step:
                            if expected_result.tag != "node":
                                continue
                            # expected_results.append(expected_result.get("TEXT"))
                            expected_results.append(self._parse_node_text(expected_result))
                    # testcase = TestCase(module.get("TEXT"), summary.get("TEXT"), steps, expected_results)
                    testcase = TestCase(self._parse_node_text(module), self._parse_node_text(summary), steps,
                                        expected_results)
                    # testcase.precondition = precondition.get("TEXT")
                    testcase.precondition = self._parse_node_text(precondition)
                    testcases_collection.append(testcase)
            else:
                for step in summary:
                    if step.tag != "node":
                        continue
                    # steps.append(step.get("TEXT"))
                    steps.append(self._parse_node_text(step))
                    for expected_result in step:
                        if expected_result.tag != "node":
                            continue
                        # expected_results.append(expected_result.get("TEXT"))
                        expected_results.append(self._parse_node_text(expected_result))
                # testcase = TestCase(module.get("TEXT"), summary.get("TEXT"), steps, expected_results)
                testcase = TestCase(self._parse_node_text(module), self._parse_node_text(summary), steps,
                                    expected_results)
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
            for child in e:
                if child.tag == "node":
                    depth += 1
                    e = child
                    break
            else:
                break
        return depth

    @staticmethod
    def _parse_node_text(e: Element):
        if not e.get('TEXT'):
            for child in e:
                if child.tag != "richcontent":
                    break
                else:
                    p_list = []
                    _find_p_label(child, p_list)
            if p_list:
                return "".join(_parse_p_text(p) for p in p_list)
        return e.get('TEXT')


# 递归查询出所有的p标签
def _find_p_label(e: Element, p_list: list):
    if e.tag != "p":
        for child in e:
            _find_p_label(child, p_list)
    else:
        p_list.append(e)


# 递归解析出p标签下的所有text
def _parse_p_text(e: Element):
    pure_text = _format_p_text(e.text)
    pure_text += _format_p_text(e.tail)
    for child in e:
        pure_text += _parse_p_text(child)
    return pure_text


def _format_p_text(s):
    if s:
        return s.lstrip("\n").strip(" ")
    return ""


if __name__ == '__main__':
    a = XMLParser("E:\document\mac_doc\webull_testcases\考勤管理-第1版.mm")
    res = a.parse_xml()
    for i in res:
        print(i)