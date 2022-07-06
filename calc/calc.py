import re
from numbers import Number
from string import digits
from typing import List, Tuple

from .input_token import Token
from .op import Bracket, Op
from .tree import GroupNode, NumNode, OpNode, Tree

AnyToken = Token[Bracket] | Token[Number] | Token[Op]
TokenGroup = List[Token[Number] | Token[Op] | "TokenGroup"]


def _put_value(root: Tree | None, new_node: NumNode | GroupNode) -> Tree:
    if root is None:
        return new_node

    rightmost_node = root
    while rightmost_node.right:
        rightmost_node = rightmost_node.right
    rightmost_node.right = new_node

    return root


def _put_op(root: Tree | None, new_node: OpNode, unary: bool = False) -> Tree:
    match root:
        case None:
            return new_node
        # If the new operation (incl. unary)
        #  has a higher precedence than the root operation,
        #  the new operation is part of the root's right operand
        # But a group has a higher precedence than any operation
        case OpNode() if (new_node.token > root.token or unary) and not isinstance(
            root, GroupNode
        ):
            root.right = _put_op(root.right, new_node, unary)
            return root
        # Otherwise, the entire expression on the left
        #  becomes the operation's left operand
        case _:
            new_node.left = root
            return new_node


def _make_node(token_group: TokenGroup) -> Tree:
    root: Tree | None = None
    prev_is_value = False

    for item in token_group:
        match item:
            # Token[Op]
            case Token() if isinstance(item.value, Op):
                root = _put_op(root, OpNode(item), unary=not prev_is_value)
                prev_is_value = False
            # Token[Number] | TokenGroup
            case _:
                new_node = _make_node(item) if isinstance(item, list) else NumNode(item)
                if isinstance(new_node, OpNode):
                    new_node.__class__ = GroupNode

                root = _put_value(root, new_node)
                prev_is_value = True

    return root


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
            tok_val, tok_start = token.value, token.start
            match tok_val:
                case Op() | Number():
                    group.append(token)

                case Bracket.P_OPEN | Bracket.S_OPEN | Bracket.C_OPEN:
                    group.append([])
                    group, bracket = group[-1], token
                    stack.append((group, bracket))

                case Bracket.P_CLOSE | Bracket.S_CLOSE | Bracket.C_CLOSE:
                    if not bracket or self._bracket_matching[tok_val] != bracket.value:
                        raise SyntaxError(
                            (self._pl + tok_start) * " " + "^\n"
                            f"unmatched '{tok_val.value}' at {tok_start}"
                        )

                    stack.pop()
                    group, bracket = stack[-1]

                case _:
                    raise NotImplementedError(
                        (self._pl + tok_start) * " " + "^\n"
                        f"unexpected token '{tok_val}' at {tok_start}"
                    )

        if bracket:
            raise SyntaxError(
                (self._pl + bracket.start) * " " + "^\n"
                f"unmatched '{bracket.value.value}' at {bracket.start}"
            )

    def _build_tree(self):
        self._tokenize()
        self._group_by_brackets()

        self._tree = _make_node(self._grouped_tokens)

    def _eval(self):
        self._build_tree()

        if not self._tree:
            return

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
