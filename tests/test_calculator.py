import pytest

import calculator


def test_add():
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0
    assert calculator.add(-2, -3) == -5


def test_subtract():
    assert calculator.subtract(10, 3) == 7
    assert calculator.subtract(0, 5) == -5
    assert calculator.subtract(5, 5) == 0


def test_multiply():
    assert calculator.multiply(4, 5) == 20
    assert calculator.multiply(-2, 3) == -6
    assert calculator.multiply(10, 0) == 0


def test_divide_normal_and_fraction():
    assert calculator.divide(10, 2) == 5
    assert pytest.approx(calculator.divide(7, 2)) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        calculator.divide(1, 0)


def test_get_operation_valid_symbols():
    assert calculator._get_operation("+") is calculator.add  # noqa: SLF001
    assert calculator._get_operation("-") is calculator.subtract  # noqa: SLF001
    assert calculator._get_operation("*") is calculator.multiply  # noqa: SLF001
    assert calculator._get_operation("/") is calculator.divide  # noqa: SLF001


def test_get_operation_invalid_symbol_raises():
    with pytest.raises(ValueError):
        calculator._get_operation("%")  # noqa: SLF001