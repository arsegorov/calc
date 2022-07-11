import pytest
from calc.op import Op, OpWithPrecedence


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
    with pytest.raises(ArithmeticError, match=r"missing the left-hand-side for '\*'"):
        Op.MULT.eval(rhs=2)


def test_eval_div_missing_args():
    with pytest.raises(ArithmeticError, match=r"missing the left-hand-side for '\/'"):
        Op.DIV.eval(rhs=2)


def test_eval_div_int_missing_args():
    with pytest.raises(ArithmeticError, match=r"missing the left-hand-side for '\/\/'"):
        Op.DIV_INT.eval(rhs=2)


def test_eval_mod_missing_args():
    with pytest.raises(ArithmeticError, match=r"missing the left-hand-side for '\%'"):
        Op.MOD.eval(rhs=2)


def test_eval_exp_missing_args():
    with pytest.raises(ArithmeticError, match=r"missing the left-hand-side for '\*\*'"):
        Op.EXP.eval(rhs=2)


def test_eval_unexpected_op():
    class MockOp(OpWithPrecedence):
        CARROT = ("^", 3)

    with pytest.raises(NotImplementedError, match=r"unexpected operation '\^'"):
        MockOp.CARROT.eval(lhs=2, rhs=2)


def test_duplicate_op():
    with pytest.raises(
        ValueError,
        match=r"cannot create multiple operations with the same symbol \('\+'\)",
    ):

        class MockOp(OpWithPrecedence):
            ADD = ("+", 0)
            UNARY_ADD = ("+", 3)


def test_gt():
    assert Op.MULT > Op.ADD


def test_lt():
    assert Op.ADD < Op.MULT


def test_eq():
    assert Op.ADD == Op.ADD
    assert Op.ADD != Op.SUB
    assert Op.ADD != 2


def test_ge():
    assert Op.MULT >= Op.ADD
    assert Op.ADD >= Op.ADD
    assert not (Op.ADD >= Op.SUB or Op.ADD < Op.SUB)


def test_le():
    assert Op.ADD <= Op.MULT
    assert Op.ADD <= Op.ADD
    assert not (Op.ADD <= Op.SUB or Op.ADD > Op.SUB)


def test_gt_unsupported():
    with pytest.raises(
        TypeError,
        match=r"'>' not supported between instances of 'Op' and 'int'"
    ):
        _ = Op.ADD > 0


def test_lt_unsupported():
    with pytest.raises(
        TypeError,
        match=r"'<' not supported between instances of 'Op' and 'int'"
    ):
        _ = Op.ADD < 0
