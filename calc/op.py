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

    @property
    def symbol(self):
        return self.value[0]

    @property
    def precedence(self):
        return self.value[1]

    def eval(self, lhs: Number | None = None, rhs: Number = 0) -> Number:
        symbol = self.symbol
        if symbol == "+":
            return (lhs or 0) + rhs
        if symbol == "-":
            return (lhs or 0) - rhs

        if lhs is None:
            raise ArithmeticError(
                f"Operator '{symbol}' requires two operands. "
                f"Only the right-hand-side operand, {rhs}, was provided"
            )

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


class Bracket(Enum):
    P_OPEN = "("
    P_CLOSE = ")"
    S_OPEN = "["
    S_CLOSE = "]"
    C_OPEN = "{"
    C_CLOSE = "}"
