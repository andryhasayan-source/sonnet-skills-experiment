# -*- coding: utf-8 -*-
"""Тесты задачи P6: нормализация телефонов."""
from conftest import load_solution

sol = load_solution("P6")


def test_common_formats():
    assert sol.normalize_phone("8 905 123-45-67") == "+79051234567"
    assert sol.normalize_phone("+7(905)1234567") == "+79051234567"
    assert sol.normalize_phone("79051234567") == "+79051234567"
    assert sol.normalize_phone("9051234567") == "+79051234567"


def test_invalid_inputs():
    assert sol.normalize_phone("12345") is None          # короткий
    assert sol.normalize_phone("19051234567") is None    # 11 цифр, не 7/8
    assert sol.normalize_phone("") is None
    assert sol.normalize_phone(None) is None


def test_normalize_list_dedup_and_order():
    raws = ["8 905 123-45-67", "+79051234567", "мусор", "9261112233"]
    result = sol.normalize_list(raws)
    assert result["valid"] == ["+79051234567", "+79261112233"]
    assert result["invalid"] == ["мусор"]


def test_normalize_list_empty():
    assert sol.normalize_list([]) == {"valid": [], "invalid": []}
