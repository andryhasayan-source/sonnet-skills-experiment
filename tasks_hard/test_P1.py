# -*- coding: utf-8 -*-
import pytest
from conftest import load_solution
sol = load_solution("P1")

def test_int_to_roman_basic():
    assert sol.int_to_roman(1) == "I"
    assert sol.int_to_roman(4) == "IV"
    assert sol.int_to_roman(9) == "IX"
    assert sol.int_to_roman(58) == "LVIII"
    assert sol.int_to_roman(1994) == "MCMXCIV"
    assert sol.int_to_roman(3999) == "MMMCMXCIX"

def test_int_to_roman_invalid():
    for bad in [0, -1, 4000, 1.5, "X", True]:
        with pytest.raises(ValueError):
            sol.int_to_roman(bad)

def test_roman_to_int_valid():
    assert sol.roman_to_int("IV") == 4
    assert sol.roman_to_int("MCMXCIV") == 1994
    assert sol.roman_to_int("MMMCMXCIX") == 3999

def test_roundtrip():
    for n in range(1, 4000):
        assert sol.roman_to_int(sol.int_to_roman(n)) == n

def test_roman_to_int_rejects_noncanonical():
    for bad in ["IIII", "VV", "LL", "DD", "IC", "IL", "XM", "VX",
                "IXI", "", "iv", "X I", "ABC", "MMMM"]:
        with pytest.raises(ValueError):
            sol.roman_to_int(bad)

def test_roman_to_int_non_str():
    with pytest.raises(ValueError):
        sol.roman_to_int(4)
