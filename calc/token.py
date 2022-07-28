from types import NotImplementedType
from typing import Generic, TypeVar


T = TypeVar("T")


class Token(Generic[T]):
    def __init__(self, value: T, start: int, end: int):
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"Token({self.value!r}, {self.start}, {self.end})"

    def __str__(self) -> str:
        return f"{self.value} ({self.start}-{self.end})"

    def __gt__(self, other) -> bool | NotImplementedType:
        if isinstance(other, Token):
            return self.value > other.value
        return NotImplemented

    def __lt__(self, other) -> bool | NotImplementedType:
        if isinstance(other, Token):
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other) -> bool | NotImplementedType:
        if isinstance(other, Token):
            return (
                self.value == other.value
                and self.start == other.start
                and self.end == other.end
            )
        return NotImplemented

    def __ge__(self, other) -> bool | NotImplementedType:
        return self > other or self == other

    def __le__(self, other) -> bool | NotImplementedType:
        return self < other or self == other
