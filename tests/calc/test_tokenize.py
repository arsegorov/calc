import pytest
from calc import Calc
from calc.op import Bracket, Op
from calc.token import Token


def test_float_wo_exp(calc_instance: Calc):
    calc_instance.input = "1.2"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(1.2, 0, 3)]


def test_float_w_exp(calc_instance: Calc):
    calc_instance.input = "0.12e1"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(1.2, 0, 6)]


def test_float_w_exp_negative(calc_instance: Calc):
    calc_instance.input = "1.2e-1"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(0.12, 0, 6)]


def test_float_w_exp_positive(calc_instance: Calc):
    calc_instance.input = ".12e+1"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(1.2, 0, 6)]


def test_float_w_exp_upper(calc_instance: Calc):
    calc_instance.input = "1.2E-1"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(0.12, 0, 6)]


def test_float_is_int_wo_exp(calc_instance: Calc):
    calc_instance.input = "12."
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(12, 0, 3)]


def test_float_is_int_w_exp(calc_instance: Calc):
    calc_instance.input = "1.2e2"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(120, 0, 5)]


def test_float_only_decimal_part(calc_instance: Calc):
    calc_instance.input = ".2"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(0.2, 0, 2)]


def test_float_only_decimal_point(calc_instance: Calc):
    with pytest.raises(SyntaxError, match=r"unexpected text at 1: '\.'"):
        calc_instance.input = "."
        calc_instance._tokenize()


def test_dec_int(calc_instance: Calc):
    calc_instance.input = "12"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(12, 0, 2)]


def test_bin(calc_instance: Calc):
    calc_instance.input = "0b11"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(3, 0, 4)]


def test_bin_invalid(calc_instance: Calc):
    with pytest.raises(ValueError, match=r"invalid literal for int\(\) with base 2"):
        calc_instance.input = "0b12"
        calc_instance._tokenize()


def test_oct(calc_instance: Calc):
    calc_instance.input = "0o17"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(15, 0, 4)]


def test_oct_invalid(calc_instance: Calc):
    with pytest.raises(ValueError, match=r"invalid literal for int\(\) with base 8"):
        calc_instance.input = "0o19"
        calc_instance._tokenize()


def test_oct_w_exp_invalid(calc_instance: Calc):
    with pytest.raises(ValueError, match=r"invalid literal for int\(\) with base 8"):
        calc_instance.input = "0o77E+1"
        calc_instance._tokenize()


def test_hex(calc_instance: Calc):
    calc_instance.input = "0xff"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(255, 0, 4)]


def test_hex_invalid(calc_instance: Calc):
    with pytest.raises(ValueError, match=r"invalid literal for int\(\) with base 16"):
        calc_instance.input = "0xfg"
        calc_instance._tokenize()


def test_dec_int_w_exp(calc_instance: Calc):
    calc_instance.input = "12e1"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(120, 0, 4)]


def test_dec_int_w_exp_negative(calc_instance: Calc):
    calc_instance.input = "12e-1"
    calc_instance._tokenize()
    assert calc_instance._tokens == [Token(1.2, 0, 5)]


def test_ops(calc_instance: Calc):
    calc_instance.input = "+ - * ** / // %"
    calc_instance._tokenize()
    assert calc_instance._tokens == [
        Token(Op.ADD, 0, 1),
        Token(Op.SUB, 2, 3),
        Token(Op.MULT, 4, 5),
        Token(Op.EXP, 6, 8),
        Token(Op.DIV, 9, 10),
        Token(Op.DIV_INT, 11, 13),
        Token(Op.MOD, 14, 15),
    ]


def test_brackets(calc_instance: Calc):
    calc_instance.input = "()[]{}"
    calc_instance._tokenize()
    assert calc_instance._tokens == [
        Token(Bracket.P_OPEN, 0, 1),
        Token(Bracket.P_CLOSE, 1, 2),
        Token(Bracket.S_OPEN, 2, 3),
        Token(Bracket.S_CLOSE, 3, 4),
        Token(Bracket.C_OPEN, 4, 5),
        Token(Bracket.C_CLOSE, 5, 6),
    ]


def test_integration(calc_instance: Calc):
    calc_instance.input = "2/[12 - 4*(1.2E-3 ** 0.5)]"
    calc_instance._tokenize()
    assert calc_instance._tokens == [
        Token(2, 0, 1),
        Token(Op.DIV, 1, 2),
        Token(Bracket.S_OPEN, 2, 3),
        Token(12, 3, 5),
        Token(Op.SUB, 6, 7),
        Token(4, 8, 9),
        Token(Op.MULT, 9, 10),
        Token(Bracket.P_OPEN, 10, 11),
        Token(0.0012, 11, 17),
        Token(Op.EXP, 18, 20),
        Token(0.5, 21, 24),
        Token(Bracket.P_CLOSE, 24, 25),
        Token(Bracket.S_CLOSE, 25, 26),
    ]
