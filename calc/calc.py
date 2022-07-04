import re
from numbers import Number
from string import digits
from typing import List, Tuple

if __name__ == "__main__":
    from op import Bracket, Op
    from tree import Tree
else:
    from .op import Bracket, Op
    from .tree import Tree


Token = Tuple[Bracket | Number | Op, int, int]
TokensList = List[Token]
GroupedTokensList = List[Tuple[Number | Op, int, int] | "GroupedTokensList"]


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
        self._tokens: TokensList = []
        self._grouped_tokens: GroupedTokensList = []
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
            self._grouped_tokens = []
            self._tree = None
            self._value = None
            self._is_evaluated = False

    _numbers_patterns = [
        # 0(b|o|x)##
        r"0[box][\da-z]+",
        # (##[.[##]] | .##)[e[+|-]##]
        r"(?:\d+(?:\.\d*)?|\.\d+)(?:e[+\-]?\d+)?",
    ]
    _ops_pattern = [
        # one of: +, -, *[*], /[/], %
        r"\+|\-|\*{1,2}|\/{1,2}|\%"
    ]
    _brackets_pattern = [
        # one of: [, ], (, ), {, }
        r"[\[\]\(\)\{\}]"
    ]
    _all_patterns = "|".join(_numbers_patterns + _ops_pattern + _brackets_pattern)
    _tokens_re = re.compile(_all_patterns, re.IGNORECASE)
    _non_whitespace_re = re.compile(r"[^\s]")
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
        text = self._input
        regexp = self._tokens_re

        def _check_for_illegal_text_between(pos: int, end_pos: int):
            gap_text = text[pos:end_pos]
            invalid_text_match = self._non_whitespace_re.search(gap_text)
            if invalid_text_match:
                raise SyntaxError(
                    (34 + pos + invalid_text_match.start()) * " " + "^\n"
                    f"unexpected text at {pos + invalid_text_match.start() + 1}: "
                    f"'{invalid_text_match[0]}'"
                )

        pos = 0
        match = regexp.search(text)
        while match:
            _check_for_illegal_text_between(pos, match.start())

            match_text = match[0]
            val = None
            if match_text[0] in f".{digits}":  # Numeric token
                if match_text[:2].lower() == "0b":
                    val = int(match_text[2:], 2)
                elif match_text[:2].lower() == "0o":
                    val = int(match_text[2:], 8)
                elif match_text[:2].lower() == "0x":
                    val = int(match_text[2:], 16)
                else:
                    val = float(match_text)
                    if val.is_integer():
                        val = int(val)
            elif match_text in self._sym_tokens:
                val = self._sym_tokens[match_text]
            else:
                raise NotImplementedError(
                    (34 + match.start()) * " " + "^\n"
                    f"unrecognized token at character {match.start()}: '{match_text}'"
                )
            self._tokens.append((val, match.start(), match.end()))

            pos = match.end()
            match = regexp.search(text, pos)

        _check_for_illegal_text_between(pos, len(text))

    _bracket_matching = {
        Bracket.P_CLOSE: Bracket.P_OPEN,
        Bracket.S_CLOSE: Bracket.S_OPEN,
        Bracket.C_CLOSE: Bracket.C_OPEN,
    }

    def _group_by_brackets(self):
        self._grouped_tokens = []
        group, bracket = self._grouped_tokens, None

        stack: List[Tuple[GroupedTokensList, Token]] = []
        stack.append((group, bracket))

        for token in self._tokens:
            t, start, _ = token
            if isinstance(t, (Number, Op)):
                group.append(token)
            elif t in (Bracket.P_OPEN, Bracket.S_OPEN, Bracket.C_OPEN):
                group, bracket = [], token
                stack[-1][0].append(group)
                stack.append((group, bracket))
            elif t in (Bracket.P_CLOSE, Bracket.S_CLOSE, Bracket.C_CLOSE):
                if not bracket or self._bracket_matching[t] != bracket[0]:
                    raise SyntaxError(
                        (34 + start) * " " + "^\n"
                        f"unmatched '{t.value}' at {start}"
                    )
                else:
                    stack.pop()
                    group, bracket = stack[-1]
            else:
                raise NotImplementedError(
                    (34 + start) * " " + "^\n" f"unexpected token at {start}"
                )

        if len(stack) > 1:
            raise SyntaxError(
                (34 + bracket[1]) * " " + "^\n"
                f"unmatched '{bracket[0].value}' at {bracket[1]}"
            )

    def _build_tree(self):
        self._tokenize()
        self._group_by_brackets()

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

            try:
                calc._build_tree()
                print(f"Tokens: {[(str(t[0]), t[1], t[2]) for t in calc._tokens]}")
                print(f"Grouped tokens: {calc._grouped_tokens}")
                print(f"> {calc.result}")
            except SyntaxError as se:
                print(se)

            s = input("\nInput the expression to evaluate: ").strip()
        else:
            print("quit")
    except EOFError:
        print("quit")


if __name__ == "__main__":
    main()
