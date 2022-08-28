
from csv import CSV
from write_xml import WriteXML


def csv2xml(csv_path: str):
    csv = CSV(csv_path)
    w = WriteXML(csv)
    w.write_xml()


if __name__ == '__main__':
    csv2xml("/Users/jameszhang/Documents/webull_testcases/webull_AMS2.0_testcase_upload_csv.csv")