"""
The example of using pytest is based on:
- John Hunt, "Advanced Guide to Python 3 Programming", Springer 2019.
"""
import pytest
from calculator import Calculator


@pytest.fixture
def calculator():
    """
    Each test is supplied with a completely new instance of a Calculator instance
    """
    print('\ncalculator fixture')
    return Calculator()


def test_initial_value(calculator):
    assert calculator.total == 0


def test_add_one(calculator):
    # calculator: <calculator.Calculator object at 0x7f08e56c0590>
    # calculate.current: 0
    # calculate.total: 0
    calculator.set(1)
    # calculate.current: 1
    # calculate.total: 0
    calculator.add()
    # calculate.current: 1
    # calculate.total: 1
    assert calculator.total == 1


def test_subtract_one(calculator):
    # calculator: <calculator.Calculator object at 0x7f08e6004cd0>
    # calculate.current: 0
    # calculate.total: 0
    calculator.set(1)
    calculator.sub()
    assert calculator.total == -1


def test_add_one_and_add_one(calculator):
    calculator.set(1)
    calculator.add()
    calculator.set(1)
    calculator.add()
    assert calculator.total == 2


@pytest.mark.skip(reason='not implemented yet')
def test_calculator_multiply(calculator):
    calculator.multiply(2, 3)
    assert calculator.total == 6


# ============================= test session starts ==============================
# collecting ... collected 5 items
#
# test_calculator_with_non_implemented_method.py::test_initial_value
# calculator fixture
# PASSED [ 20%]
# test_calculator_with_non_implemented_method.py::test_add_one
# calculator fixture
# PASSED      [ 40%]
# test_calculator_with_non_implemented_method.py::test_subtract_one
# calculator fixture
# PASSED [ 60%]
# test_calculator_with_non_implemented_method.py::test_add_one_and_add_one
# calculator fixture
# PASSED [ 80%]
# test_calculator_with_non_implemented_method.py::test_calculator_multiply SKIPPED [100%]
# Skipped: not implemented yet
#
#
# ========================= 4 passed, 1 skipped in 0.01s =========================
