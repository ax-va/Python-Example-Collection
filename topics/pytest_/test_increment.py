"""
The example of using pytest is based on:
- John Hunt, "Advanced Guide to Python 3 Programming", Springer 2019.
"""
from increment import increment


def test_increment_int_3():
    assert increment(3) == 4
