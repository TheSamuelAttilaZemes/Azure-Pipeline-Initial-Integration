import math

import pytest

import calculator


# -------- Core operations --------


def test_add_basic_and_negative():
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0
    assert calculator.add(-2, -3) == -5


def test_subtract_basic_and_zero():
    assert calculator.subtract(10, 3) == 7
    assert calculator.subtract(0, 5) == -5
    assert calculator.subtract(5, 5) == 0


def test_multiply_basic_and_zero():
    assert calculator.multiply(4, 5) == 20
    assert calculator.multiply(-2, 3) == -6
    assert calculator.multiply(10, 0) == 0


def test_divide_basic_and_fraction():
    assert calculator.divide(10, 2) == 5
    assert pytest.approx(calculator.divide(7, 2)) == 3.5


def test_divide_by_zero_raises():
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
    with pytest.raises(ValueError):
        calculator.percentage(10, 0)


def test_sqrt_basic_and_non_integer():
    assert calculator.sqrt(4) == 2
    assert pytest.approx(calculator.sqrt(2)) == pytest.approx(math.sqrt(2))


def test_sqrt_negative_raises():
    with pytest.raises(ValueError):
        calculator.sqrt(-1)


# -------- Expression evaluator --------


def test_evaluate_expression_simple_ops():
    assert calculator.evaluate_expression("2 + 3") == 5.0
    assert calculator.evaluate_expression("10 - 4") == 6.0
    assert calculator.evaluate_expression("3 * 4") == 12.0
    assert calculator.evaluate_expression("8 / 2") == 4.0


def test_evaluate_expression_with_functions_and_constants():
    assert calculator.evaluate_expression("2 * sqrt(9)") == 6.0
    result = calculator.evaluate_expression("pi * 2")
    assert pytest.approx(result) == math.pi * 2


def test_evaluate_expression_empty_and_whitespace():
    with pytest.raises(ValueError):
        calculator.evaluate_expression("")
    with pytest.raises(ValueError):
        calculator.evaluate_expression("   ")


def test_evaluate_expression_unknown_function_raises():
    with pytest.raises(Exception):
        calculator.evaluate_expression("unknown_func(2)")

# -------- CLI tests (to increase coverage) --------


def test_run_cli_quit_immediately(monkeypatch, capsys):
    """
    Run the CLI and quit immediately with 'q'.

    This exercises:
    - the startup banner
    - the main loop
    - the quit branch
    """
    inputs = iter(["q"])

    def fake_input(_prompt: str) -> str:
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    calculator.run_cli()

    captured = capsys.readouterr()
    # Check that the CLI printed the goodbye message
    assert "Goodbye." in captured.out


def test_run_cli_expression_mode(monkeypatch, capsys):
    """
    Run the CLI in expression mode:

    1) choose '2' for expr mode
    2) enter '2 + 3'
    3) then 'q' to quit

    This exercises:
    - mode selection
    - expression evaluation path
    """
    inputs = iter([
        "2",        # choose expression mode
        "2 + 3",    # expression
        "q",        # quit
    ])

    def fake_input(_prompt: str) -> str:
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    calculator.run_cli()

    captured = capsys.readouterr()
    # Should have printed the result of 2 + 3 and then the goodbye message
    assert "= 5.0" in captured.out
    assert "Goodbye." in captured.out
def test_run_cli_basic_add(monkeypatch, capsys):
    """
    Exercise mode 1 (a op b) with a valid '+' operation, then quit.
    """
    inputs = iter([
        "1",      # first loop: choose mode 1 
        "2",      # first number
        "+",      # operator
        "3",      # second number
        "q",      # second loop: quit
    ])

    def fake_input(_prompt: str) -> str:
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    calculator.run_cli()

    captured = capsys.readouterr()
    # Should print result of 2 + 3 and then goodbye
    assert "= 5.0" in captured.out
    assert "Goodbye." in captured.out


def test_run_cli_percentage_error(monkeypatch, capsys):
    """
    Exercise percentage operation with whole=0 => error path.
    """
    inputs = iter([
        "1",      # mode 1
        "10",     # first number (part)
        "%",      # percentage operation
        "0",      # second number (whole -> 0 => error)
        "q",      # then quit
    ])

    def fake_input(_prompt: str) -> str:
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    calculator.run_cli()

    captured = capsys.readouterr()
    # Should have printed an error message from percentage()
    assert "Error:" in captured.out
    assert "Whole cannot be zero" in captured.out


def test_run_cli_unsupported_operation(monkeypatch, capsys):
    """
    Exercise unsupported operation branch, which raises ValueError
    and is caught by the CLI's exception handler.
    """
    inputs = iter([
        "1",      # mode 1
        "1",      # first number
        "x",      # unsupported operator
        "1",      # second number
        "q",      # then quit
    ])

    def fake_input(_prompt: str) -> str:
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    calculator.run_cli()

    captured = capsys.readouterr()
    # CLI should show an error for unsupported operation
    assert "Error:" in captured.out
    assert "Unsupported operation: x" in captured.out
