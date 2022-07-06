from abc import ABC, abstractmethod
from numbers import Number


class Tree(ABC):
    def __init__(self, left: "Tree | None" = None, right: "Tree | None" = None):
        self._left = left
        self._right = right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left: "Tree | None"):
        self._left = left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right: "Tree | None"):
        self._right = right

    @abstractmethod
    def eval(self) -> Number:
        pass  # pragma: no cover
