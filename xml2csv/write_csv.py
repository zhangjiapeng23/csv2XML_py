import os.path

from xml_parser import XMLParser


class WriteCSV:
    _csv_field_map = {
        "id": "case_id",
        "Summary": "summary",
        "Assignee": "assignee",
        "Reporter": "reporter",
        "Issue Type": "issue_type",
        "Component": "component",
        "Description": "precondition",
        "Test Type": "test_type",
        "Action": "steps",
        "Data": "data",
        "Expected Result": "expected_results",
        "Test Repository Path": "test_repository_path"
    }

    def __init__(self, xml_path: str, **kwargs):
        self._testcases = XMLParser(xml_path).parse_xml()
        self._additional_info = kwargs
        self._file_dir = os.path.dirname(xml_path)
        self._file_name = os.path.splitext(os.path.basename(xml_path))[0] + ".csv"

    def write_csv(self):
        # 读取模版
        csv_line_template = ""
        with open("template/testcase_template.csv", encoding='utf-8') as f:
            csv_title = f.readline()

        csv_field_list = csv_title.split(",")
        csv_field_list = [field.strip(" ") for field in csv_field_list]
        csv_field_list = [field.strip("\ufeff") for field in csv_field_list]
        csv_field_list = [field.strip("\n") for field in csv_field_list]
        csv_field_position = self._get_csv_field_position(csv_field_list)
        for field in csv_field_position:
            if csv_line_template != "":
                csv_line_template += ","
            csv_line_template += "{%s}" % field

        # 将固定字段的值填入
        for k, v in self._additional_info.items():
            if k == "assignee":
                assignee = v
            elif k == "reporter":
                reporter = v
            elif k == "issue_type":
                issue_type = v
            elif k == "component":
                component = v
            elif k == "test_type":
                test_type = v
            elif k == "data":
                data = v
            elif k == "test_repository_path":
                test_repository_path = v

        csv_file_path = os.path.join(self._file_dir, self._file_name)

        with open(csv_file_path, 'w', encoding='utf-8') as f:
            f.write(csv_title)
            for case in self._testcases:
                if case.precondition:
                    precondition = f"\"前置条件:\n{case.precondition}\""
                else:
                    precondition = f"\"前置条件:\n无\""

                steps = "\""
                for index, step in enumerate(case.steps, start=1):
                    steps += f"步骤{index}:\n{step}"
                    steps += "\n\n"
                steps += "\""

                expected_results = "\""
                for index, respected_result in enumerate(case.expected_results, start=1):
                    expected_results += f"预期结果{index}:\n{respected_result}"
                    expected_results += "\n\n"
                expected_results += "\""

                case_line = csv_line_template.format(case_id=case.case_id, summary=f"【{case.module}】{case.summary}",
                                                     assignee=assignee, reporter=reporter, issue_type=issue_type,
                                                     component=component, precondition=precondition,
                                                     test_type=test_type, steps=steps, data=data,
                                                     expected_results=expected_results,
                                                     test_repository_path=test_repository_path)

                f.write(case_line)
                f.write("\n")

    def _get_csv_field_position(self, origin_field_list: list[str]):
        csv_field_position = []
        for index, field in enumerate(origin_field_list):
            csv_field_position.append((index, self._csv_field_map[field]))

        csv_field_position.sort(key=lambda x: x[0])

        return [field[1] for field in csv_field_position]

