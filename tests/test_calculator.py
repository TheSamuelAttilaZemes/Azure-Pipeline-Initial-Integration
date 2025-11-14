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


# -------- CLI tests (run_cli on main) --------


def test_run_cli_quit_immediately(monkeypatch, capsys):
    """
    User enters 'q' straight away.
    Exercises:
    - main loop
    - quit branch
    """
    inputs = iter(["q"])

    def fake_input(_prompt: str) -> str:
        return next(inputs)

    # Patch builtins.input so run_cli reads from our inputs iterator
    monkeypatch.setattr("builtins.input", fake_input)

    calculator.run_cli()

    captured = capsys.readouterr()
    assert "Goodbye." in captured.out


def test_run_cli_simple_add(monkeypatch, capsys):
    """
    User enters a valid expression '2 + 3' then 'q'.
    Exercises:
    - parsing of '<number> <op> <number>'
    - _get_operation('+')
    - success path printing '= 5.0'
    """
    inputs = iter([
        "2 + 3",  # first iteration: valid calculation
        "q",      # second iteration: quit
    ])

    def fake_input(_prompt: str) -> str:
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    calculator.run_cli()

    captured = capsys.readouterr()
    assert "= 5.0" in captured.out
    assert "Goodbye." in captured.out


def test_run_cli_invalid_format_then_quit(monkeypatch, capsys):
    """
    User enters 'bad input' (len(parts) != 3) then 'q'.
    Exercises:
    - the 'len(parts) != 3' ValueError branch
    - the generic 'Error: ...' handler
    """
    inputs = iter([
        "bad input",  # invalid -> should trigger ValueError about format
        "q",          # quit
    ])

    def fake_input(_prompt: str) -> str:
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    calculator.run_cli()

    captured = capsys.readouterr()
    assert "Error:" in captured.out
    assert "Input must be in format" in captured.out
    assert "Goodbye." in captured.out
