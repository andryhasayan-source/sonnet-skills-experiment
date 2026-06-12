# -*- coding: utf-8 -*-
"""Тесты задачи P3: валидатор JSON-конфига."""
import json
import pytest
from conftest import load_solution

sol = load_solution("P3")

GOOD = {
    "app_name": "shop",
    "port": 8080,
    "debug": False,
    "database": {"host": "localhost", "port": 5432},
    "admins": ["a@b.ru"],
}


def test_load_config_ok(tmp_path):
    p = tmp_path / "cfg.json"
    p.write_text(json.dumps(GOOD), encoding="utf-8")
    assert sol.load_config(str(p))["app_name"] == "shop"


def test_load_config_missing_file(tmp_path):
    with pytest.raises(ValueError):
        sol.load_config(str(tmp_path / "no_such.json"))


def test_load_config_broken_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{это не json", encoding="utf-8")
    with pytest.raises(ValueError):
        sol.load_config(str(p))


def test_validate_good():
    assert sol.validate_config(GOOD) == []


def test_validate_collects_multiple_errors():
    bad = {"app_name": "", "port": 99999, "debug": "yes",
           "database": {"host": ""}, "admins": []}
    errors = sol.validate_config(bad)
    assert len(errors) >= 5  # все проблемы найдены, не только первая


def test_validate_bad_admin_email():
    cfg = dict(GOOD, admins=["not-an-email"])
    assert len(sol.validate_config(cfg)) >= 1


def test_validate_never_crashes():
    for weird in [{}, {"port": "80"}, {"database": "нет"}, {"admins": "x"}]:
        result = sol.validate_config(weird)
        assert isinstance(result, list)
        assert len(result) >= 1
