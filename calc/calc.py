import re
from numbers import Number
from typing import List

if __name__ == "__main__":
    from op import Bracket, Op
    from tree import Tree
else:
    from .op import Bracket, Op
    from .tree import Tree


class OpNode(Tree):
    def __init__(
        self, op: Op, leftTree: "Tree | None" = None, rightTree: "Tree | None" = None
    ):
        super().__init__(leftTree, rightTree)
        self._op = op


class NumNode(Tree):
    def __init__(self, value: Number):
        super().__init__()
        self._value = value


class Calc:
    def __init__(self, input_string: str = ""):
        self._input = input_string
        self._tokens: List[Bracket | Op | Number] = []
        self._tree: Tree | None = None
        self._value: Number | None = None
        self._is_evaluated = False

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, input_string: str):
        if input_string != self._input:
            self._input = input_string
            self._tokens = []
            self._tree = None
            self._value = None
            self._is_evaluated = False

    _numbers_patterns = [
        # `0[b|o|x]##`
        r"0[box][\da-f]+",
        # `##[.[##]][e[+|-]##]`
        r"(?:\d+(?:\.\d*)?|\.\d+)(?:e[+\-]?\d+)?",
    ]
    _ops_pattern = [
        # `+` | `-` | `*[*]` | `/[/]` | `%`
        r"\+|\-|\*{1,2}|\/{1,2}|\%"
    ]
    _brackets_pattern = [
        # `[` | `]` | `(` | `)` | `{` | `}`
        r"[\[\]\(\)\{\}]"
    ]
    _all_patterns = "|".join(_numbers_patterns + _ops_pattern + _brackets_pattern)
    _tokens_re = re.compile(_all_patterns, re.IGNORECASE)
    _sym_tokens = {
        "[": Bracket.S_OPEN,
        "(": Bracket.P_OPEN,
        "{": Bracket.C_OPEN,
        "]": Bracket.S_CLOSE,
        ")": Bracket.P_CLOSE,
        "}": Bracket.C_CLOSE,
        "+": Op.ADD,
        "-": Op.SUB,
        "*": Op.MULT,
        "/": Op.DIV,
        "//": Op.DIV_INT,
        "%": Op.MOD,
        "**": Op.EXP,
    }

    def _tokenize(self):
        # TODO: detect invalid tokens

        for match in self._tokens_re.finditer(self._input):
            s = match[0]
            token = None
            if s[0] in ".0123456789abcdefABCDEF":
                if s[:2] in ("0b", "0B"):
                    token = int(s[2:], 2)
                elif s[:2] in ("0o", "0O"):
                    token = int(s[2:], 8)
                elif s[:2] in ("0x", "0X"):
                    token = int(s[2:], 16)
                else:
                    token = float(s)
                    if token.is_integer():
                        token = int(token)
            elif s in self._sym_tokens:
                token = self._sym_tokens[s]
            else:
                raise ValueError(
                    f"Unrecognized token: {s} between {match.start()} and {match.end()}"
                )

            self._tokens.append((token, match.start(), match.end()))

    def _build_tree(self):
        self._tokenize()

    def _eval(self):
        self._build_tree()

    @property
    def result(self):
        if not self._is_evaluated:
            self._eval()
            self._is_evaluated = True
        return self._value


def main():
    from json import dumps
    from pprint import pprint

    calc = Calc()
    try:
        s = input("Input the expression to evaluate: ").strip()
        while s:
            calc.input = s
            calc._tokenize()
            print(f"Tokens: {[(str(t[0]), t[1], t[2]) for t in calc._tokens]}")
            print(f"> {calc.result}")
            s = input("Input the expression to evaluate: ").strip()
        else:
            print("quit")
    except EOFError:
        print("quit")


if __name__ == "__main__":
    main()
