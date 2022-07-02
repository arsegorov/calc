from abc import ABC


class Tree(ABC):
    def __init__(self, leftTree: "Tree | None" = None, rightTree: "Tree | None" = None):
        self._left = leftTree
        self._right = rightTree

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, leftTree: "Tree | None"):
        self._left = leftTree

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, rightTree: "Tree | None"):
        self._right = rightTree
