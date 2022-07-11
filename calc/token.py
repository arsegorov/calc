from typing import Generic, TypeVar


T = TypeVar("T")


class Token(Generic[T]):
    def __init__(self, value: T, start: int, end: int):
        self.value = value
        self.start = start
        self.end = end

    def __gt__(self, other):
        if isinstance(other, Token):
            return self.value > other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Token):
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Token):
            return (
                self.value == other.value
                and self.start == other.start
                and self.end == other.end
            )
        return NotImplemented

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other
