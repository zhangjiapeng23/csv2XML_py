
from csv2xml.csv import CSV
from csv2xml.write_xml import WriteXML


def csv2xml(csv_path: str):
    csv = CSV(csv_path)
    w = WriteXML(csv)
    w.write_xml()


if __name__ == '__main__':
    csv2xml("E:\document\mac_doc\webull_testcases\hcm_employee_testcases.csv")