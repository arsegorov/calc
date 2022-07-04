from typing import Generic, TypeVar


T = TypeVar("T")


class Token(Generic[T]):
    def __init__(self, value: T, start: int, end: int):
        self.value = value
        self.start = start
        self.end = end
