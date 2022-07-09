from enum import Enum
from numbers import Number


class Op(Enum):
    ADD = ("+", 0)
    SUB = ("-", 0)
    MULT = ("*", 1)
    DIV = ("/", 1)
    MOD = ("%", 1)
    DIV_INT = ("//", 1)
    EXP = ("**", 2)

    def __init__(self, symbol, precedence):
        self.symbol: str = symbol
        self.precedence: int = precedence

    def eval(self, lhs: Number | None = None, rhs: Number = 0) -> Number:
        symbol = self.symbol
        if symbol == "+":
            return (lhs or 0) + rhs
        if symbol == "-":
            return (lhs or 0) - rhs

        if lhs is None:
            raise ArithmeticError(f"missing the left-hand-side for '{symbol}'")

        if symbol == "*":
            return lhs * rhs
        if symbol == "/":
            return lhs / rhs
        if symbol == "//":
            return lhs // rhs
        if symbol == "%":
            return lhs % rhs
        if symbol == "**":
            return lhs**rhs

        raise NotImplementedError(f"unexpected operation '{symbol}'")

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.precedence > other.precedence
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.precedence < other.precedence
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.symbol == other.symbol and self.precedence == other.precedence
        return NotImplemented

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)


class Bracket(Enum):
    P_OPEN = "("
    P_CLOSE = ")"
    S_OPEN = "["
    S_CLOSE = "]"
    C_OPEN = "{"
    C_CLOSE = "}"
