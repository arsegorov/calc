from enum import Enum
from numbers import Number


class Op(Enum):
    ADD = "+"
    SUB = "-"
    MULT = "*"
    DIV = "/"
    MOD = "%"
    DIV_INT = "//"
    EXP = "**"

    def eval(self, lhs: Number | None, rhs: Number) -> Number:
        if self.value == "+":
            return (lhs or 0) + rhs
        if self.value == "-":
            return (lhs or 0) - rhs

        if lhs is None:
            raise ArithmeticError(
                f"Operator '{self.value}' requires two operands. "
                f"Only the right-hand-side operand, {rhs}, was provided"
            )

        if self.value == "*":
            return lhs * rhs
        if self.value == "/":
            return lhs / rhs
        if self.value == "//":
            return lhs // rhs
        if self.value == "%":
            return lhs % rhs
        if self.value == "**":
            return lhs**rhs


class Bracket(Enum):
    P_OPEN = "("
    P_CLOSE = ")"
    S_OPEN = "["
    S_CLOSE = "]"
    C_OPEN = "{"
    C_CLOSE = "}"
