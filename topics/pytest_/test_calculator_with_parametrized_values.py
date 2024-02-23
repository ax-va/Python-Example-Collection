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


@pytest.mark.parametrize(
    'input1,input2,expected',
    [
        (3, 1, 4),
        (3, 2, 5),
    ]
)
def test_calculator_add(calculator, input1, input2, expected):
    calculator.set(input1)
    calculator.add()
    calculator.set(input2)
    calculator.add()
    assert calculator.total == expected


# ============================= test session starts ==============================
# collecting ... collected 2 items
#
# test_calculator_with_parametrized_values.py::test_calculator_add[3-1-4]
# calculator fixture
# PASSED [ 50%]
# test_calculator_with_parametrized_values.py::test_calculator_add[3-2-5]
# calculator fixture
# PASSED [100%]
#
# ============================== 2 passed in 0.01s ===============================
