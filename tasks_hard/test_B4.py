# -*- coding: utf-8 -*-
from conftest import load_solution
sol = load_solution("B4")

def test_assign_no_operators():
    d = sol.Dispatcher()
    assert d.assign(1) is None

def test_balancing():
    d = sol.Dispatcher()
    d.add_operator(10)
    d.add_operator(20)
    assert d.assign(1) == 10   # оба по 0 -> ранее добавленный
    assert d.assign(2) == 20   # теперь 10 загружен, 20 свободнее
    assert d.assign(3) == 10   # снова равны (по 1) -> ранее добавленный
    assert d.load(10) == 2
    assert d.load(20) == 1

def test_assign_idempotent():
    d = sol.Dispatcher()
    d.add_operator(10)
    d.add_operator(20)
    op = d.assign(1)
    assert d.assign(1) == op   # тот же тикет — тот же оператор, без переназначения
    assert d.load(op) == 1

def test_close():
    d = sol.Dispatcher()
    d.add_operator(10)
    d.assign(1)
    assert d.close(1) is True
    assert d.close(1) is False
    assert d.load(10) == 0

def test_add_operator_idempotent():
    d = sol.Dispatcher()
    d.add_operator(10)
    d.add_operator(10)
    d.assign(1)
    assert d.load(10) == 1

def test_remove_operator_returns_tickets():
    d = sol.Dispatcher()
    d.add_operator(10)
    d.assign(1)
    d.assign(2)
    tickets = d.remove_operator(10)
    assert set(tickets) == {1, 2}
    assert d.assign(3) is None   # операторов больше нет

def test_remove_absent():
    d = sol.Dispatcher()
    assert d.remove_operator(999) == []

def test_reassign_after_close_balances():
    d = sol.Dispatcher()
    d.add_operator(10)
    d.add_operator(20)
    d.assign(1)   # 10
    d.assign(2)   # 20
    d.close(1)    # 10 свободен
    assert d.assign(3) == 10
