# -*- coding: utf-8 -*-
from conftest import load_solution
sol = load_solution("B8")

def test_starts_new():
    fsm = sol.OrderFSM()
    assert fsm.status("o1") == "new"

def test_valid_transition():
    fsm = sol.OrderFSM()
    assert fsm.transition("o1", "paid") is True
    assert fsm.status("o1") == "paid"

def test_invalid_transition_blocked():
    fsm = sol.OrderFSM()
    assert fsm.transition("o1", "shipped") is False   # из new нельзя сразу shipped
    assert fsm.status("o1") == "new"

def test_unknown_status():
    fsm = sol.OrderFSM()
    assert fsm.transition("o1", "teleported") is False

def test_can_transition():
    fsm = sol.OrderFSM()
    assert fsm.can_transition("o1", "paid") is True
    assert fsm.can_transition("o1", "delivered") is False

def test_history_only_successful():
    fsm = sol.OrderFSM()
    fsm.transition("o1", "paid")
    fsm.transition("o1", "shipped")
    fsm.transition("o1", "cancelled")   # из shipped нельзя -> не в истории
    assert fsm.history("o1") == ["new", "paid", "shipped"]

def test_is_terminal():
    fsm = sol.OrderFSM()
    assert fsm.is_terminal("o1") is False
    fsm.transition("o1", "cancelled")
    assert fsm.is_terminal("o1") is True

def test_full_happy_path():
    fsm = sol.OrderFSM()
    for s in ["paid", "shipped", "delivered"]:
        assert fsm.transition("o1", s) is True
    assert fsm.is_terminal("o1") is True
    assert fsm.history("o1") == ["new", "paid", "shipped", "delivered"]

def test_orders_independent():
    fsm = sol.OrderFSM()
    fsm.transition("o1", "paid")
    assert fsm.status("o2") == "new"
