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


# ------- New development features -------


def power(base: float, exponent: float) -> float:
    """Return base raised to exponent."""
    return base**exponent


def percentage(part: float, whole: float) -> float:
    """
    Return what percentage 'part' is of 'whole'.

    Example:
        percentage(25, 200) -> 12.5

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
    # functions
    "sqrt": math.sqrt,
    "pow": pow,
    # constants
    "pi": math.pi,
    "e": math.e,
}


def evaluate_expression(expr: str) -> float:
    """
    Safely evaluate a simple numerical expression.

    Supports: +, -, *, /, **, parentheses, and sqrt(), pi, e.

    Uses a restricted eval environment (no builtins, no variables).
    Raises:
        ValueError: If the expression is empty or only whitespace.
    """
    if not expr or not expr.strip():
        raise ValueError("Expression cannot be empty.")

    # Restricted evaluation context
    return float(eval(expr, {"__builtins__": {}}, _ALLOWED_NAMES))  # noqa: PGH001, S307


def run_cli() -> None:
    """
    Enhanced CLI for development branch (interactive, not covered by tests).
    """
    print("Advanced Calculator (development branch)")
    print("Core operations: add, subtract, multiply, divide")
    print("Extra operations: power, percentage, sqrt, expr (expression evaluator)")
    print("Type 'q' to quit.\n")

    while True:
        print("Choose mode:")
        print(" 1) a op b  (basic or power/percentage)")
        print(" 2) expr    (expression evaluator, e.g. '2 + 3 * sqrt(4)')")
        print(" q) quit")
        choice = input("mode> ").strip().lower()

        if choice in {"q", "quit", "exit"}:
            print("Goodbye.")
            break

        try:
            if choice == "2" or choice == "expr":
                expr = input("expression> ").strip()
                result = evaluate_expression(expr)
                print(f"= {result}\n")
                continue

            # mode 1: a op b
            a_str = input("first number> ").strip()
            op = input("operation (+, -, *, /, **, %)> ").strip()
            b_str = input("second number> ").strip()

            a = float(a_str)
            b = float(b_str)

            if op == "+":
                result = add(a, b)
            elif op == "-":
                result = subtract(a, b)
            elif op == "*":
                result = multiply(a, b)
            elif op == "/":
                result = divide(a, b)
            elif op == "**":
                result = power(a, b)
            elif op == "%":
                result = percentage(a, b)
            else:
                raise ValueError(f"Unsupported operation: {op}")

            print(f"= {result}\n")

        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    run_cli()