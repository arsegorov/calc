import re
from numbers import Number
from string import digits
from typing import List, Tuple

from .input_token import Token
from .num_node import NumNode
from .op import Bracket, Op
from .op_node import OpNode
from .tree import Tree

AnyToken = Token[Bracket] | Token[Number] | Token[Op]
TokenGroup = List[Token[Number] | Token[Op] | "TokenGroup"]


class Calc:
    def __init__(self, prompt: str = "Type an expression: ", input_string: str = ""):
        self._input = input_string
        self._tokens: List[AnyToken] = []
        self._grouped_tokens: TokenGroup = []
        self._tree: Tree | None = None
        self._value: Number | None = None
        self._is_evaluated = False
        self._prompt: str = prompt
        self._pl: int = len(prompt)

    def read_input(self):
        input_string = input(self._prompt)
        if input_string != self._input:
            self._input = input_string
            self._tokens = []
            self._grouped_tokens = []
            self._tree = None
            self._value = None
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

    @property
    def prompt_length(self):
        return self._pl

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, new_prompt: str):
        self._prompt = new_prompt
        self._pl = len(new_prompt)

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
        self._tokens = []

        text = self._input
        regexp = self._tokens_re

        def _check_for_illegal_text_between(pos: int, end_pos: int):
            gap_text = text[pos:end_pos]
            invalid_text_match = self._non_whitespace_re.search(gap_text)
            if invalid_text_match:
                raise SyntaxError(
                    (self._pl + pos + invalid_text_match.start()) * " " + "^\n"
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
                    (self._pl + match.start()) * " " + "^\n"
                    f"unrecognized token at character {match.start()}: '{match_text}'"
                )
            self._tokens.append(Token(val, match.start(), match.end()))

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

        stack: List[Tuple[TokenGroup, Token[Bracket]]] = []
        stack.append((group, bracket))

        for token in self._tokens:
            t, start = token.value, token.start
            if isinstance(t, (Number, Op)):
                group.append(token)
            elif t in (Bracket.P_OPEN, Bracket.S_OPEN, Bracket.C_OPEN):
                group, bracket = [], token
                stack[-1][0].append(group)
                stack.append((group, bracket))
            elif t in (Bracket.P_CLOSE, Bracket.S_CLOSE, Bracket.C_CLOSE):
                if not bracket or self._bracket_matching[t] != bracket.value:
                    raise SyntaxError(
                        (self._pl + start) * " " + "^\n"
                        f"unmatched '{t.value}' at {start}"
                    )
                else:
                    stack.pop()
                    group, bracket = stack[-1]
            else:
                raise NotImplementedError(
                    (self._pl + start) * " " + "^\n" f"unexpected token at {start}"
                )

        if len(stack) > 1:
            raise SyntaxError(
                (self._pl + bracket.start) * " " + "^\n"
                f"unmatched '{bracket.value}' at {bracket.start}"
            )

    def _build_tree(self):
        self._tokenize()
        self._group_by_brackets()

        def _make_node(token_group: TokenGroup) -> Tree:
            def _put_num(tree: Tree | None, item: Token[Number] | Tree) -> Tree:
                if tree is None:
                    return item if isinstance(item, Tree) else NumNode(item)

                node = tree
                while node.right:
                    node = node.right
                node.right = item if isinstance(item, Tree) else NumNode(item)

                return tree

            def _put_op(
                tree: Tree | None, item: Token[Op], is_unary: bool = False
            ) -> Tree:
                if tree is None:
                    return OpNode(item)

                if isinstance(tree, NumNode):
                    return OpNode(item, left=tree)

                if isinstance(tree, OpNode):
                    if tree.token < item or is_unary:
                        tree.right = _put_op(tree.right, item, is_unary)
                    else:
                        tree = OpNode(item, left=tree)
                    return tree

            res: Tree | None = None
            is_unary_op = True

            for item in token_group:
                if isinstance(item, Token) and isinstance(item.value, Number):
                    res = _put_num(res, item)
                    is_unary_op = False
                elif isinstance(item, Token) and isinstance(item.value, Op):
                    res = _put_op(res, item, is_unary_op)
                    is_unary_op = True
                else:
                    res = _put_num(res, _make_node(item))

            return res

        self._tree = _make_node(self._grouped_tokens)

    def _eval(self):
        self._build_tree()
        try:
            self._value = self._tree.eval()
            self._is_evaluated = True
        except ArithmeticError as ae:
            print((self._pl + ae.args[1]) * " " + "^\n" + ae.args[0])

    @property
    def result(self):
        if not self._is_evaluated:
            self._eval()
        return self._value
