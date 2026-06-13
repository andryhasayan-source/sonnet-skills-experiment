# -*- coding: utf-8 -*-
import pytest
from conftest import load_solution
sol = load_solution("B1")

def test_add_returns_total():
    c = sol.Cart()
    assert c.add(1, "apple", 2) == 2
    assert c.add(1, "apple", 3) == 5

def test_add_invalid_qty():
    c = sol.Cart()
    with pytest.raises(ValueError):
        c.add(1, "apple", 0)

def test_remove_partial_and_full():
    c = sol.Cart()
    c.add(1, "milk", 5)
    assert c.remove(1, "milk", 2) == 3
    assert c.remove(1, "milk", 10) == 0     # ушло в 0 -> удалён
    assert "milk" not in c.items(1)

def test_remove_absent():
    c = sol.Cart()
    assert c.remove(1, "ghost", 1) == 0

def test_items_is_copy():
    c = sol.Cart()
    c.add(1, "apple", 1)
    snap = c.items(1)
    snap["apple"] = 999
    assert c.items(1)["apple"] == 1

def test_users_independent():
    c = sol.Cart()
    c.add(1, "apple", 2)
    c.add(2, "apple", 5)
    assert c.total_qty(1) == 2
    assert c.total_qty(2) == 5

def test_summary_empty():
    c = sol.Cart()
    assert sol.cart_summary(c, 1) == "Корзина пуста."

def test_summary_order_and_total():
    c = sol.Cart()
    c.add(1, "apple", 3)   # 150
    c.add(1, "milk", 1)    # 80
    summary = sol.cart_summary(c, 1)
    lines = summary.split("\n")
    assert lines[0] == "apple x3 = 150 руб."
    assert lines[1] == "milk x1 = 80 руб."
    assert lines[-1] == "Итого: 230 руб."

def test_clear():
    c = sol.Cart()
    c.add(1, "apple", 2)
    c.clear(1)
    assert c.total_qty(1) == 0
