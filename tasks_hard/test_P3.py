# -*- coding: utf-8 -*-
from conftest import load_solution
sol = load_solution("P3")

def test_basic():
    assert sol.evaluate("2+2") == 4.0
    assert sol.evaluate("2 + 3 * 4") == 14.0
    assert sol.evaluate("(2 + 3) * 4") == 20.0
    assert sol.evaluate("10 / 4") == 2.5

def test_precedence_assoc():
    assert sol.evaluate("100 / 10 / 2") == 5.0   # левоассоц.
    assert sol.evaluate("2 - 3 - 4") == -5.0

def test_unary_minus():
    assert sol.evaluate("-5") == -5.0
    assert sol.evaluate("3 * -2") == -6.0
    assert sol.evaluate("-(2+3)") == -5.0
    assert sol.evaluate("2--3") == 5.0

def test_decimals():
    assert sol.evaluate("1.5 + 2.5") == 4.0
    assert abs(sol.evaluate("0.1 + 0.2") - 0.3) < 1e-9

def test_div_zero_none():
    assert sol.evaluate("1/0") is None
    assert sol.evaluate("5 / (3 - 3)") is None

def test_syntax_errors_none():
    for bad in ["", "  ", "2+", "*5", "2 3", "(2+3", "2+3)", "()",
                "2 ** 3", "abc", "2 + + ", "."]:
        assert sol.evaluate(bad) is None, bad

def test_no_eval_in_source():
    import inspect, re
    src = inspect.getsource(sol)
    # запрещаем вызовы eval(/exec(/literal_eval, но не имя функции evaluate
    assert not re.search(r"(?<![A-Za-z_])eval\s*\(", src)
    assert not re.search(r"(?<![A-Za-z_])exec\s*\(", src)
    assert "literal_eval" not in src

def test_non_str():
    assert sol.evaluate(123) is None
    assert sol.evaluate(None) is None
