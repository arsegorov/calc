from numbers import Number

from op import Op
from parsed_token import Token
from tree import Tree


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
            raise SyntaxError(
                f"missing the right-hand-side for '{self.token.value.symbol}'",
                self.token.end,
            )

        try:
            return self.token.value.eval(
                self.left.eval() if self.left else None, self.right.eval()
            )
        except SyntaxError as se:
            raise SyntaxError(se.args[0], self.token.end)
