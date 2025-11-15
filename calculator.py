from __future__ import annotations

import math
from typing import Callable, Dict


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference a - b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product a * b."""
    return a * b


def divide(a: float, b: float) -> float:
    """
    Return the quotient a / b.

    Raises:
        ValueError: If b == 0.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def power(base: float, exponent: float) -> float:
    """Return base raised to exponent."""
    return base**exponent


def percentage(part: float, whole: float) -> float:
    """
    Return what percentage 'part' is of 'whole'.

    Raises:
        ValueError: If whole == 0.
    """
    if whole == 0:
        raise ValueError("Whole cannot be zero when computing percentage.")
    return (part / whole) * 100.0


def sqrt(x: float) -> float:
    """
    Return the square root of x.

    Raises:
        ValueError: If x < 0.
    """
    if x < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(x)


_ALLOWED_NAMES: Dict[str, float | Callable[..., float]] = {
    "sqrt": math.sqrt,
    "pow": pow,
    "pi": math.pi,
    "e": math.e,
}


def evaluate_expression(expr: str) -> float:
    """
    Evaluate a simple numerical expression in a restricted environment.

    Raises:
        ValueError: If the expression is empty or only whitespace.
    """
    if not expr or not expr.strip():
        raise ValueError("Expression cannot be empty.")
    return float(eval(expr, {"__builtins__": {}}, _ALLOWED_NAMES))  # noqa: PGH001, S307


if __name__ == "__main__":
    # Minimal manual sanity check entrypoint
    print("Test-and-ops calculator module. Run 'pytest --cov=calculator --cov-fail-under=80'.")
