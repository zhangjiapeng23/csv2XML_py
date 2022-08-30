import uuid


class Node:

    def __init__(self, name, order=0):
        self._name = name
        # 每个节点都生成一唯一的UUID
        self._id = "ID_" + str(uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=self._name))
        # 父节点的uuid
        self._parent_id = None
        self._order = order

    @property
    def name(self):
        return self._name

    @property
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, val):
        self._parent_id = val

    @property
    def id(self):
        return self._id

    @property
    def order(self):
        return self._order

    def __str__(self):
        return f"Name: {self.name}, id: {self._id}, parent_id: {self._parent_id}"


if __name__ == '__main__':
    node = Node(name="james")
    print(node)


