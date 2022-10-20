
from csv2xml.csv import CSV
from csv2xml.write_xml import WriteXML
from xml2csv.write_csv import WriteCSV


def csv2xml(csv_path: str):
    w = WriteXML(csv_path)
    w.write_xml()


def xml2csv(xml_path: str):
    additional_info = {
        "assignee": "zhangjiapeng",
        "reporter": "zhangjiapeng",
        "issue_type": "Test",
        "component": "PMS-权限管理",
        "test_type": "Manual",
        "data": "无",
        "test_repository_path": "HCM/常规/2022/权限优化"
    }
    w = WriteCSV(xml_path, **additional_info)
    w.write_csv()


if __name__ == '__main__':
    xml2csv("E:\document\mac_doc\webull_testcases\测试颜色.mm")
    # csv2xml("E:\document\mac_doc\webull_testcases\PMS-系统与数据权限.csv")