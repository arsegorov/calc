from numbers import Number

from .input_token import Token
from .op import Op
from .tree import Tree


class OpNode(Tree):
    def __init__(
        self,
        token: Token[Op],
        left: Tree | None = None,
        right: Tree | None = None,
    ):
        super().__init__(left, right)
        self.token = token

    def eval(self) -> Number:
        if not self.right:
            raise ArithmeticError(
                f"missing the right-hand-side for '{self.token.value.symbol}'",
                self.token.end - 1,
            )

        try:
            return self.token.value.eval(
                self.left.eval() if self.left else None, self.right.eval()
            )
        except ArithmeticError as ae:
            if len(ae.args) > 1:
                raise
            else:
                raise ArithmeticError(ae.args[0], self.token.start)
