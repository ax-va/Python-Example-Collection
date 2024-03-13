from calculator import Calculator


def test_initial_value():
    calc = Calculator()
    assert calc.total == 0


def test_add_one():
    calc = Calculator()
    calc.set(1)
    calc.add()
    if calc.total != 1:
        raise AssertionError()


def test_subtract_one():
    calc = Calculator()
    calc.set(1)
    calc.sub()
    assert calc.total == -1


def test_add_one_and_add_one():
    calc = Calculator()
    calc.set(1)
    calc.add()
    calc.set(1)
    calc.add()
    assert calc.total == 2


# Environment variable "testpaths" is to start the search for tests
# recursively, # unless they match environment variable "norecursedirs".
# In those directories, it will search for files that match
# the naming conventions test_*.py or *_test.py files.
