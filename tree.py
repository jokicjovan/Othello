from queue1 import Queue

class TreeNode(object):
    __slots__ = '_parent', '_children', '_data'

    def __init__(self, data):
        self._parent = None
        self._children = []
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def children(self):
        return self._children

    def is_root(self):
        return self._parent is None

    def is_leaf(self):
        return len(self._children) == 0

    def add_child(self, x):
        x.parent = self
        self._children.append(x)


class Tree(object):
    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    def is_empty(self):
        return self._root is None

    def depth(self, x):
        if x.is_root():
            return 0
        else:
            return 1 + self.depth(x.parent)

    def _height(self, x):
        if x.is_leaf():
            return 0
        else:
            return 1 + max(self._height(c) for c in x.children)

    def height(self):
        return self._height(self._root)

    def preorder(self, x):
        if not self.is_empty():
            print(x.data)
            for c in x.children:
                self.preorder(c)

    def postorder(self, x):
        if not self.is_empty():
            for c in x.children:
                self.postorder(c)
            print(x.data)

    def breadth_first(self):
        to_visit = Queue()
        to_visit.enqueue(self._root)
        while not to_visit.is_empty():
            e = to_visit.dequeue()
            print(e.data)

            for c in e.children:
                to_visit.enqueue(c)
