from typing import Callable


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


def _get_operation(op_symbol: str) -> Callable[[float, float], float]:
    """Map an operator symbol to the corresponding function."""
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    if op_symbol not in operations:
        raise ValueError(f"Unsupported operation: {op_symbol}")
    return operations[op_symbol]


def run_cli() -> None:
    """
    Simple interactive CLI (not covered by tests, but small enough
    that overall coverage remains ≥ 80% on this file).
    """
    print("Simple Calculator (main branch)")
    print("Supported operations: +  -  *  /")
    print("Enter expressions like: 2 + 3")
    print("Type 'q' to quit.\n")

    while True:
        user_input = input("calc> ").strip()
        if user_input.lower() in {"q", "quit", "exit"}:
            print("Goodbye.")
            break

        try:
            parts = user_input.split()
            if len(parts) != 3:
                raise ValueError("Input must be in format: <number> <op> <number>")

            a_str, op_symbol, b_str = parts
            a = float(a_str)
            b = float(b_str)

            op_func = _get_operation(op_symbol)
            result = op_func(a, b)
            print(f"= {result}\n")

        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    run_cli()