import pytest
from calc.op import Op


def test_eval():
    assert Op.ADD.eval(rhs=2) == 2
    assert Op.ADD.eval(1, 2) == 3
    assert Op.SUB.eval(1, 2) == -1
    assert Op.SUB.eval(rhs=2) == -2
    assert Op.MULT.eval(1, 2) == 2
    assert Op.DIV.eval(1, 2) == 0.5
    assert Op.DIV_INT.eval(1, 2) == 0
    assert Op.MOD.eval(5, 2) == 1
    assert Op.EXP.eval(2, 2) == 4


def test_eval_mult_missing_args():
    with pytest.raises(
        ArithmeticError,
        match=r"Operator '\*' requires two operands\. "
        r"Only the right-hand-side operand, 2, was provided",
    ):
        Op.MULT.eval(rhs=2)


def test_eval_div_missing_args():
    with pytest.raises(
        ArithmeticError,
        match=r"Operator '\/' requires two operands\. "
        r"Only the right-hand-side operand, 2, was provided",
    ):
        Op.DIV.eval(rhs=2)


def test_eval_div_int_missing_args():
    with pytest.raises(
        ArithmeticError,
        match=r"Operator '\/\/' requires two operands\. "
        r"Only the right-hand-side operand, 2, was provided",
    ):
        Op.DIV_INT.eval(rhs=2)


def test_eval_mod_missing_args():
    with pytest.raises(
        ArithmeticError,
        match=r"Operator '\%' requires two operands\. "
        r"Only the right-hand-side operand, 2, was provided",
    ):
        Op.MOD.eval(rhs=2)


def test_eval_exp_missing_args():
    with pytest.raises(
        ArithmeticError,
        match=r"Operator '\*\*' requires two operands\. "
        r"Only the right-hand-side operand, 2, was provided",
    ):
        Op.EXP.eval(rhs=2)
