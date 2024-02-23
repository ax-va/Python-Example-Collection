"""
The example of using pytest is based on:
- John Hunt, "Advanced Guide to Python 3 Programming", Springer 2019.
"""
import pytest
from calculator import Calculator

# autouse=True will activate a fixture for all tests that can see it.
# If autouse=False (which is the default) then an explicit reference
# in a test function (or method etc.) is required to activate the fixture.


@pytest.fixture(scope='session', autouse=True)
def session_scope_fixture():
    # Run once for the test session
    print('\nsession_scope_fixture')


@pytest.fixture(scope='module', autouse=True)
def module_scope_fixture():
    # Run once for the module
    print('module_scope_fixture')


@pytest.fixture(scope='class', autouse=True)
def class_scope_fixture():
    # Run for each new instance of a test class created
    print('class_scope_fixture')


@pytest.fixture
def calculator():
    print('calculator fixture')
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
# test_calculator_with_fixture_scope.py::test_initial_value
# session_scope_fixture
# module_scope_fixture
# class_scope_fixture
# calculator fixture
# PASSED         [ 25%]
# test_calculator_with_fixture_scope.py::test_add_one class_scope_fixture
# calculator fixture
# PASSED               [ 50%]
# test_calculator_with_fixture_scope.py::test_subtract_one class_scope_fixture
# calculator fixture
# PASSED          [ 75%]
# test_calculator_with_fixture_scope.py::test_add_one_and_add_one class_scope_fixture
# calculator fixture
# PASSED   [100%]
#
# ============================== 4 passed in 0.01s ===============================
