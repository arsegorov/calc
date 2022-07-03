from abc import ABC


class Tree(ABC):
    def __init__(self, left: "Tree | None" = None, right: "Tree | None" = None):
        self._left = left
        self._right = right

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
