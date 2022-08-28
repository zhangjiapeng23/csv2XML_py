import os.path
import re

from node import Node


class CSV:
    _node_field = ["Summary", "Action", "Expected Result"]
    _module_name_pattern = re.compile(r"^【(.*)】(.*)")

    def __init__(self, file_path: str):
        self._file_name = self.get_file_name(file_path)
        self._file_dir = self.get_file_dir(file_path)
        self._csv_title = ""
        self._csv_body = []
        self._node_position = {}
        self._node_list = []
        with open(file_path, "r", encoding="utf-8") as f:
            # 将csv的 title 存入到_csv_title, 内容存入到_csv_body中
            for index, line in self.read_line(f):
                if index == 0:
                    self._csv_title = line
                else:
                    self._csv_body.append(line)
        _csv_title_list = self._csv_title.split(",")
        # 确定要使用到字段列在每行数据到索引
        for field in self._node_field:
            self._node_position[field] = _csv_title_list.index(field)

    def get_node_tree(self):
        module_record = {}
        # 将文件名作为脑图到根节点
        root = Node(name=self.file_name)
        self._node_list.append(root)
        for line in self.line_gen():
            action_record = []
            # 每行数据都按照 summary，action, expected result 的顺序来生成node
            for field in self._node_field:
                index = self._node_position[field]
                if field == "Summary":
                    # split origin summary to【module】and summary
                    match = self._module_name_pattern.search(line[index])
                    if match:
                        module_name = match.groups()[0]
                        summary_name = match.groups()[1]
                    else:
                        module_name = "Common"
                        summary_name = line[index]
                        if summary_name == "":
                            continue

                    # 当模块名已经存在时，不再重复创建，仅创建summery的title部分
                    if module_name in module_record.keys():
                        parent_id = module_record.get(module_name)
                    else:
                        # 新创建的模块节点的父节点即为root节点
                        parent_id = root.id
                        node_obj = Node(name=module_name)
                        node_obj.parent_id = parent_id
                        parent_id = node_obj.id
                        self._node_list.append(node_obj)
                        module_record[module_name] = node_obj.id

                    # add case id
                    summary_name = f"(ID {line[0]}) {summary_name}"
                    node_obj = Node(name=summary_name)
                    node_obj.parent_id = parent_id
                    parent_id = node_obj.id
                    self._node_list.append(node_obj)
                elif field == "Action":
                    actions = line[index]
                    # 将每个步骤切分为单个的node
                    for action in self.parse_str_gen(actions, "步骤"):
                        node_obj = Node(name=action)
                        node_obj.parent_id = parent_id
                        # 记录下每个步骤的id顺序，为预期结果找到对应的parent_id
                        action_record.append(node_obj.id)
                        self._node_list.append(node_obj)

                elif field == "Expected Result":
                    expects = line[index]
                    # 将每个预期结果切分为单个的node
                    for index, expect in enumerate(self.parse_str_gen(expects, "预期结果")):
                        node_obj = Node(name=expect)
                        if index < len(action_record):
                            node_obj.parent_id = action_record[index]
                        else:
                            node_obj.parent_id = action_record[-1]

                        self._node_list.append(node_obj)
                else:
                    name = line[index]
                    node_obj = Node(name=name)
                    node_obj.parent_id = parent_id
                    parent_id = node_obj.id
                    self._node_list.append(node_obj)
        return self._node_list

    def line_gen(self):
        for line in self.csv_body:
            yield self.split_line(line)

    @staticmethod
    def parse_str_gen(s: str, split: str):
        line_pattern = re.compile(r".+\n?")
        split_pattern = re.compile(r".*(%s[0-9]).*" % split)
        line_gen = line_pattern.finditer(s)
        single_ = ""
        for line_match in line_gen:
            line = line_match.group().strip(" ")
            line = line.replace("\"", "")
            if split_pattern.search(line):
                if len(single_) > 0:
                    yield single_
                    single_ = line
                else:
                    single_ += line
            else:
                single_ += line

        yield single_

    @staticmethod
    def split_line(line: str):
        line_list = []
        flag = True
        real_s = ""
        for s in line.split(","):
            real_s += s
            for i in s:
                if i == '"':
                    flag = not flag
            if flag:
                line_list.append(real_s)
                real_s = ""
        return line_list

    @staticmethod
    def read_line(f):
        flag = True
        index = 0
        real_line = ""
        for line in f.readlines():
            for s in line:
                if s == '"':
                    flag = not flag
            real_line += line
            if flag:
                yield index, real_line
                index += 1
                real_line = ""

    @staticmethod
    def get_file_name(file_path: str) -> str:
        file = os.path.basename(file_path)
        file_name = os.path.splitext(file)[0]
        return file_name

    @staticmethod
    def get_file_dir(file_path: str) -> str:
        return os.path.dirname(file_path)

    @property
    def file_name(self):
        return self._file_name

    @property
    def csv_title(self):
        return self._csv_title

    @property
    def csv_body(self):
        return self._csv_body

    @property
    def file_dir(self):
        return self._file_dir

