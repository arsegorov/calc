from enum import Enum
from numbers import Number
from types import NotImplementedType


class OpWithPrecedence(Enum):
    def __init__(self, symbol, precedence):
        cls = self.__class__
        if any(symbol == e.symbol for e in cls):
            raise ValueError(
                f"cannot create multiple operations with the same symbol ('{symbol}')"
            )

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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    def __str__(self) -> str:
        return f"'{self.symbol}'"

    def __gt__(self, other) -> bool | NotImplementedType:
        if isinstance(other, OpWithPrecedence):
            return self.precedence > other.precedence
        return NotImplemented

    def __lt__(self, other) -> bool | NotImplementedType:
        if isinstance(other, OpWithPrecedence):
            return self.precedence < other.precedence
        return NotImplemented

    def __ge__(self, other) -> bool | NotImplementedType:
        return self > other or self == other

    def __le__(self, other) -> bool | NotImplementedType:
        return self < other or self == other


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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    def __str__(self) -> str:
        return f"'{self.value}'"
