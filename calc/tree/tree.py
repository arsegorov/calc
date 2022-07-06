from abc import ABC, abstractmethod
from numbers import Number


class Tree(ABC):
    """Abstract base class for the syntax tree nodes."""

    def __init__(self, left: "Tree | None" = None, right: "Tree | None" = None):
        """Creates a tree node.

        Args:
            left (Tree | None, optional): The initial left subtree. Defaults to None.
            right (Tree | None, optional): The initial right subtree. Defaults to None.
        """
        self._left = left
        self._right = right

    @property
    def left(self):
        """The current left subtree."""
        return self._left

    @left.setter
    def left(self, left: "Tree | None"):
        """Updates the left subtree.

        Args:
            left (Tree | None): The new left subtree.
        """
        self._left = left

    @property
    def right(self):
        """The current right subtree."""
        return self._right

    @right.setter
    def right(self, right: "Tree | None"):
        """Updates the right subtree.

        Args:
            right (Tree | None): The new right subtree.
        """
        self._right = right

    @abstractmethod
    def eval(self) -> Number:
        """Evaluates the numerical value.

        Evaluates and returns the numerical value of the expression stored in the tree.

        Returns:
            Number: The numerical value
        """
        pass  # pragma: no cover
