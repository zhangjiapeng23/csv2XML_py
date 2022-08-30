import datetime
import os.path
from xml.etree import ElementTree as ET
from collections import defaultdict

from csv2xml.csv import CSV

TAG = "node"


class WriteXML:

    def __init__(self, csv: CSV):
        self._node_list = csv.get_node_tree()
        self._dist = csv.file_dir
        # xml 的根节点，free mind 的固定格式
        self._root = ET.Element("map", attrib={"version": "freeplane 1.9.13"})
        self._tree = ET.ElementTree(self._root)
        # key: id, val: element boj
        self._node_seen = defaultdict()
        self._file_name = "temp.mm"
        self._timestamp = str(int(datetime.datetime.now().timestamp()))

    def write_xml(self):
        for node in self._node_list:
            # 没有parent id, 为思维导图的根节点
            if not node.parent_id:
                # 生成的 xml 的文件地址
                self._file_name = os.path.join(self._dist, node.name + ".mm")
                # 生成root 节点下的二级节点
                e = ET.SubElement(self._root, TAG, attrib={"TEXT": node.name, "LOCALIZED_STYLE_REF": "default",
                                                           "FOLDED": "false", "ID": node.id,
                                                           "CREATED": self._timestamp,
                                                           "MODIFIED": self._timestamp})
                self._node_seen[node.id] = e
            else:
                # 通过seen_node找到当前节点的父节点
                parent_node = self._node_seen.get(node.parent_id)
                # 在对应的父节点下生成当前节点
                e = ET.SubElement(parent_node, TAG, attrib={"TEXT": node.name, "ID": node.id,
                                                            "CREATED": self._timestamp,
                                                            "MODIFIED": self._timestamp})
                self._node_seen[node.id] = e

        self._tree.write(self._file_name, encoding="utf-8")

