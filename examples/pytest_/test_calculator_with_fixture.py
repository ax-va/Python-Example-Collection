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


# ============================= test session starts ==============================
# collecting ... collected 4 items
#
# test_calculator_with_fixture.py::test_initial_value
# calculator fixture
# PASSED               [ 25%]
# test_calculator_with_fixture.py::test_add_one
# calculator fixture
# PASSED                     [ 50%]
# test_calculator_with_fixture.py::test_subtract_one
# calculator fixture
# PASSED                [ 75%]
# test_calculator_with_fixture.py::test_add_one_and_add_one
# calculator fixture
# PASSED         [100%]
#
# ============================== 4 passed in 0.01s ===============================
