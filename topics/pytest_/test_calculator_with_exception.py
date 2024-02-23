import pytest
from calculator import Calculator


@pytest.fixture
def calculator():
    """
    Each test is supplied with a completely new instance of a Calculator instance
    """
    print('\ncalculator fixture')
    return Calculator()


def test_value_error(calculator):
    with pytest.raises(ValueError):
        calculator.raise_value_error()


# ============================= test session starts ==============================
# collecting ... collected 1 item
#
# test_calculator_with_exception.py::test_value_error
# calculator fixture
# PASSED               [100%]
#
# ============================== 1 passed in 0.01s ===============================
