from enum import Enum
from numbers import Number


class OpWithPrecedence(Enum):
    def __init__(self, symbol, precedence):
        cls = self.__class__
        if any(symbol == e.symbol for e in cls):
            raise ValueError(f"operation '{symbol}' already exists")

        self.symbol: str = symbol
        self.precedence: int = precedence

    def eval(self, lhs: Number | None = None, rhs: Number = 0) -> Number:
        if self.symbol not in "+-" and lhs is None:
            raise ArithmeticError(f"missing the left-hand-side for '{self.symbol}'")

        match self.symbol:
            case "+":
                return (lhs or 0) + rhs
            case "-":
                return (lhs or 0) - rhs
            case "*":
                return lhs * rhs
            case "/":
                return lhs / rhs
            case "//":
                return lhs // rhs
            case "%":
                return lhs % rhs
            case "**":
                return lhs**rhs

        raise NotImplementedError(f"unexpected operation '{self.symbol}'")

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
            return self.symbol == other.symbol
        return NotImplemented

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)


class Op(OpWithPrecedence):
    ADD = ("+", 0)
    SUB = ("-", 0)
    MULT = ("*", 1)
    DIV = ("/", 1)
    MOD = ("%", 1)
    DIV_INT = ("//", 1)
    EXP = ("**", 2)


class Bracket(Enum):
    P_OPEN = "("
    P_CLOSE = ")"
    S_OPEN = "["
    S_CLOSE = "]"
    C_OPEN = "{"
    C_CLOSE = "}"
