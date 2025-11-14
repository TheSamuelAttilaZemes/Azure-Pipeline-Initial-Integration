import pytest
from calculator import add, subtract, multiply, divide

def test_add_basic():
    assert add(2, 3) == 5


def test_subtract_basic():
    assert subtract(10, 3) == 7


def test_multiply_basic():
    assert multiply(4, 5) == 20


def test_divide_basic():
    assert divide(10, 2) == 5


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)