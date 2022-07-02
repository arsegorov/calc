from hypothesis import given, strategies as st

from calc.calc import Calc


@given(st.text(max_size=10))
def test_new_input(s):
    assert True
