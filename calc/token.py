from typing import Generic, TypeVar


T = TypeVar("T")


class Token(Generic[T]):
    def __init__(self, value: T, start: int, end: int):
        self.value = value
        self.start = start
        self.end = end

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return (
                self.value == other.value
                and self.start == other.start
                and self.end == other.end
            )
        return NotImplemented

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
