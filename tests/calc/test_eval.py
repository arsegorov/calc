from calc import Calc


def test_group_first(calc_instance: Calc):
    calc_instance.input = "(3 + 4) * 3"
    assert calc_instance.result == 21


def test_group_second(calc_instance: Calc):
    calc_instance.input = "2**(3 + 4)"
    assert calc_instance.result == 128


def test_precedence(calc_instance: Calc):
    calc_instance.input = "2 * 3 + 4 * 2**2"
    assert calc_instance.result == 22


def test_precedence_w_group(calc_instance: Calc):
    calc_instance.input = "2 * (3 + 4) + 7 * 2**2"
    assert calc_instance.result == 42


def test_unary_precedence(calc_instance: Calc):
    calc_instance.input = "3 * -2"
    assert calc_instance.result == -6


def test_double_unary(calc_instance: Calc):
    calc_instance.input = "3 * --2"
    assert calc_instance.result == 6


def test_only_number_in_brackets(calc_instance: Calc):
    calc_instance.input = "(2)"
    assert calc_instance.result == 2
