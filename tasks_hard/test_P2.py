# -*- coding: utf-8 -*-
from conftest import load_solution
sol = load_solution("P2")

def test_simple_merge():
    assert sol.deep_merge({"a":1,"b":2}, {"b":3,"c":4}) == {"a":1,"b":3,"c":4}

def test_nested_merge():
    base = {"db": {"host": "local", "port": 5432}, "debug": False}
    over = {"db": {"port": 6000}, "debug": True}
    assert sol.deep_merge(base, over) == {
        "db": {"host": "local", "port": 6000}, "debug": True}

def test_dict_replaced_by_scalar():
    assert sol.deep_merge({"a": {"x": 1}}, {"a": 5}) == {"a": 5}

def test_scalar_replaced_by_dict():
    assert sol.deep_merge({"a": 5}, {"a": {"x": 1}}) == {"a": {"x": 1}}

def test_list_replaced_not_merged():
    out = sol.deep_merge({"xs": [1,2,3]}, {"xs": [9]})
    assert out["xs"] == [9]

def test_no_mutation():
    base = {"db": {"opts": [1,2]}}
    over = {"db": {"opts": [3]}}
    b_copy = {"db": {"opts": [1,2]}}
    sol.deep_merge(base, over)
    assert base == b_copy  # base не тронут

def test_list_copy_not_reference():
    over_list = [1, 2]
    out = sol.deep_merge({}, {"xs": over_list})
    out["xs"].append(99)
    assert over_list == [1, 2]  # вернулась копия

def test_delete_marker():
    out = sol.deep_merge({"a": 1, "b": 2}, {"b": sol.DELETE})
    assert out == {"a": 1}

def test_delete_nested():
    base = {"cfg": {"a": 1, "b": 2}}
    over = {"cfg": {"b": sol.DELETE}}
    assert sol.deep_merge(base, over) == {"cfg": {"a": 1}}

def test_delete_absent_key_noop():
    out = sol.deep_merge({"a": 1}, {"z": sol.DELETE})
    assert out == {"a": 1}
