from hypothesis import given, strategies as st

from calc.calc import Calc


@given(st.text(max_size=10))
def test_initial_input(s):
    calc = Calc(input_string=s)
    assert calc._input == s
    assert calc._tokens == []
    assert calc._tree is None
    assert calc._value is None
    assert not calc._is_evaluated


def test_new_input(calc_instance: Calc):
    calc_instance.input = "2 + 3 * 5"
    calc_instance.result

    new_string = "123 - 456"
    calc_instance.input = new_string
    assert calc_instance._input == new_string
    assert calc_instance._tokens == []
    assert calc_instance._tree is None
    assert calc_instance._value is None
    assert not calc_instance._is_evaluated
