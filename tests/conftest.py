import pytest

from calc.calc import Calc


@pytest.fixture(scope="session")
def calc_instance():
    return Calc()
