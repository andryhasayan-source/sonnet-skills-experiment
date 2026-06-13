# -*- coding: utf-8 -*-
import pytest
from conftest import load_solution
sol = load_solution("P6")

def test_examples():
    assert sol.pretty_duration(90061, max_units=2) == "1d 1h"
    assert sol.pretty_duration(86400) == "1d 0h"
    assert sol.pretty_duration(3661) == "1h 1m"
    assert sol.pretty_duration(3600) == "1h 0m"
    assert sol.pretty_duration(61) == "1m 1s"
    assert sol.pretty_duration(59) == "59s"

def test_zero():
    assert sol.pretty_duration(0) == "0s"
    assert sol.pretty_duration(0.4) == "0s"

def test_floor_fraction():
    assert sol.pretty_duration(59.9) == "59s"

def test_max_units_one():
    assert sol.pretty_duration(90061, max_units=1) == "1d"
    assert sol.pretty_duration(3661, max_units=1) == "1h"

def test_max_units_three():
    assert sol.pretty_duration(90061, max_units=3) == "1d 1h 1m"

def test_tail_shorter_than_max_units():
    # 61 c, max_units=3: старшая ненулевая m, дальше s, дни/часы нет
    assert sol.pretty_duration(61, max_units=3) == "1m 1s"

def test_errors():
    with pytest.raises(ValueError):
        sol.pretty_duration(-1)
    with pytest.raises(ValueError):
        sol.pretty_duration(100, max_units=0)
