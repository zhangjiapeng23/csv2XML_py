from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element


class XMLParser:

    def __init__(self, file_path: str):
        tree = ET.parse(file_path)
        self._root = tree.getroot()
        self._testcases_collection = []


    def get_depth(self, e: Element):
        pass

