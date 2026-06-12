# -*- coding: utf-8 -*-
"""Тесты задачи P1: отчёт по продажам из CSV."""
import pytest
from conftest import load_solution

sol = load_solution("P1")

CSV_OK = """date,city,product,amount
2026-01-15,Москва,Ноутбук,55000
2026-01-16,Казань,Мышь,1200
2026-01-17,Москва,Мышь,1300
2026-01-18,Казань,Ноутбук,60000
"""

CSV_DIRTY = """date,city,product,amount
2026-01-15,Москва,Ноутбук,55000
битая строка без полей
2026-01-16,Казань,Мышь,не_число
2026-01-17,Москва,Клавиатура,2500
"""


def make_csv(tmp_path, content, name="sales.csv"):
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return str(p)


def test_load_sales_basic(tmp_path):
    path = make_csv(tmp_path, CSV_OK)
    rows = sol.load_sales(path)
    assert len(rows) == 4
    assert rows[0]["city"] == "Москва"
    assert isinstance(rows[0]["amount"], float)
    assert rows[0]["amount"] == 55000.0


def test_load_sales_skips_bad_rows(tmp_path):
    path = make_csv(tmp_path, CSV_DIRTY)
    rows = sol.load_sales(path)
    assert len(rows) == 2  # битые строки молча пропущены
    products = {r["product"] for r in rows}
    assert products == {"Ноутбук", "Клавиатура"}


def test_total_by_city(tmp_path):
    rows = sol.load_sales(make_csv(tmp_path, CSV_OK))
    totals = sol.total_by_city(rows)
    assert totals["Москва"] == pytest.approx(56300.0)
    assert totals["Казань"] == pytest.approx(61200.0)


def test_top_product(tmp_path):
    rows = sol.load_sales(make_csv(tmp_path, CSV_OK))
    assert sol.top_product(rows) == "Ноутбук"  # 115000 против 2500


def test_top_product_empty():
    assert sol.top_product([]) is None
