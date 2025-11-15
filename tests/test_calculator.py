
import math

import pytest

import calculator


# -------- Core operations --------


def test_add_basic_and_negative():
    # Normal case
    assert calculator.add(2, 3) == 5
    # Mixed signs
    assert calculator.add(-1, 1) == 0
    # Both negative
    assert calculator.add(-2, -3) == -5


def test_subtract_basic_and_zero():
    # Normal case
    assert calculator.subtract(10, 3) == 7
    # Subtract from zero
    assert calculator.subtract(0, 5) == -5
    # Zero difference
    assert calculator.subtract(5, 5) == 0


def test_multiply_basic_and_zero():
    # Normal case
    assert calculator.multiply(4, 5) == 20
    # Negative * positive
    assert calculator.multiply(-2, 3) == -6
    # Multiply by zero
    assert calculator.multiply(10, 0) == 0


def test_divide_basic_and_fraction():
    # Normal division
    assert calculator.divide(10, 2) == 5
    # Fraction result
    assert pytest.approx(calculator.divide(7, 2)) == 3.5


def test_divide_by_zero_raises():
    # Error path for divide
    with pytest.raises(ValueError):
        calculator.divide(1, 0)


# -------- Extra features --------


def test_power_basic_and_zero_exponent():
    assert calculator.power(2, 3) == 8
    assert calculator.power(10, 0) == 1


def test_percentage_basic_and_100_percent():
    assert pytest.approx(calculator.percentage(25, 200)) == 12.5
    assert pytest.approx(calculator.percentage(50, 50)) == 100.0


def test_percentage_zero_whole_raises():
    # Error path for percentage
    with pytest.raises(ValueError):
        calculator.percentage(10, 0)


def test_sqrt_basic_and_non_integer():
    # Perfect square
    assert calculator.sqrt(4) == 2
    # Non-perfect square
    assert pytest.approx(calculator.sqrt(2)) == pytest.approx(math.sqrt(2))


def test_sqrt_negative_raises():
    # Error path for sqrt
    with pytest.raises(ValueError):
        calculator.sqrt(-1)


# -------- Expression evaluator --------


def test_evaluate_expression_simple_ops():
    assert calculator.evaluate_expression("2 + 3") == 5.0
    assert calculator.evaluate_expression("10 - 4") == 6.0
    assert calculator.evaluate_expression("3 * 4") == 12.0
    assert calculator.evaluate_expression("8 / 2") == 4.0


def test_evaluate_expression_with_functions_and_constants():
    # 2 * sqrt(9) = 2 * 3 = 6
    assert calculator.evaluate_expression("2 * sqrt(9)") == 6.0

    # pi * 2 (approx)
    result = calculator.evaluate_expression("pi * 2")
    assert pytest.approx(result) == math.pi * 2


def test_evaluate_expression_empty_and_whitespace():
    # Empty string
    with pytest.raises(ValueError):
        calculator.evaluate_expression("")

    # Whitespace-only string
    with pytest.raises(ValueError):
        calculator.evaluate_expression("   ")


def test_evaluate_expression_unknown_function_raises():
    # This exercises the error coming from eval for unknown names
    with pytest.raises(Exception):
        calculator.evaluate_expression("unknown_func(2)")