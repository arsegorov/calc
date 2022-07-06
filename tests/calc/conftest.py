import pytest

from calc import Calc


@pytest.fixture(scope="session")
def calc_instance():
    return Calc()
