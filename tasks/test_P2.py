# -*- coding: utf-8 -*-
"""Тесты задачи P2: фильтрация логов."""
from conftest import load_solution

sol = load_solution("P2")

LINES = [
    "2026-06-01 12:30:45 | ERROR | payment | Card declined",
    "2026-06-01 12:31:00 | INFO | auth | Login ok",
    "2026-06-01 12:32:10 | ERROR | auth | Bad token",
    "строка не по формату",
    "2026-06-01 12:33:00 | WARNING | payment | Slow response",
]


def test_parse_line_ok():
    rec = sol.parse_line(LINES[0])
    assert rec == {"timestamp": "2026-06-01 12:30:45", "level": "ERROR",
                   "module": "payment", "message": "Card declined"}


def test_parse_line_bad():
    assert sol.parse_line("мусор без разделителей") is None


def test_filter_by_level():
    recs = sol.filter_logs(LINES, level="ERROR")
    assert len(recs) == 2
    assert all(r["level"] == "ERROR" for r in recs)


def test_filter_by_level_and_module():
    recs = sol.filter_logs(LINES, level="ERROR", module="auth")
    assert len(recs) == 1
    assert recs[0]["message"] == "Bad token"


def test_filter_no_filters_skips_broken():
    recs = sol.filter_logs(LINES)
    assert len(recs) == 4  # битая строка выпала


def test_count_by_level():
    counts = sol.count_by_level(LINES)
    assert counts == {"ERROR": 2, "INFO": 1, "WARNING": 1}
