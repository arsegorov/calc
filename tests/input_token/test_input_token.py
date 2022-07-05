from calc.input_token import Token


def test_init():
    t = Token("a", 0, 1)
    assert t.value == "a"
    assert t.start == 0
    assert t.end == 1
