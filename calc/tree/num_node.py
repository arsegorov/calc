from numbers import Number

from ..input_token import Token
from .tree import Tree


class NumNode(Tree):
    def __init__(self, token: Token[Number]):
        super().__init__()
        self.token = token

    def eval(self) -> Number:
        return self.token.value
