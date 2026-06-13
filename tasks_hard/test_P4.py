# -*- coding: utf-8 -*-
import pytest
from conftest import load_solution
sol = load_solution("P4")

def test_parse_valid():
    assert sol.parse_version("1.2.3") is not None
    assert sol.parse_version("0.0.0") is not None
    assert sol.parse_version("1.2.3-alpha.1+build.7") is not None

def test_parse_invalid():
    for bad in ["1.2", "1.2.3.4", "01.2.3", "1.02.3", "1.2.x",
                "", "1.2.-3", "v1.2.3", "1.2.3-", "1..3"]:
        assert sol.parse_version(bad) is None, bad

def test_compare_core():
    assert sol.compare("1.0.0", "2.0.0") == -1
    assert sol.compare("2.1.0", "2.0.9") == 1
    assert sol.compare("1.2.3", "1.2.3") == 0

def test_prerelease_less_than_release():
    assert sol.compare("1.0.0-alpha", "1.0.0") == -1
    assert sol.compare("1.0.0", "1.0.0-rc.1") == 1

def test_prerelease_ordering():
    assert sol.compare("1.0.0-alpha", "1.0.0-alpha.1") == -1
    assert sol.compare("1.0.0-alpha.1", "1.0.0-alpha.beta") == -1  # числ < нечисл
    assert sol.compare("1.0.0-alpha.beta", "1.0.0-beta") == -1
    assert sol.compare("1.0.0-beta.2", "1.0.0-beta.11") == -1      # численно

def test_build_metadata_ignored():
    assert sol.compare("1.0.0+a", "1.0.0+b") == 0
    assert sol.compare("1.0.0-x+1", "1.0.0-x+2") == 0

def test_compare_invalid_raises():
    with pytest.raises(ValueError):
        sol.compare("1.2", "1.2.3")
