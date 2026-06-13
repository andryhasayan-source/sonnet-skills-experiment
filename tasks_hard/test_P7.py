# -*- coding: utf-8 -*-
import pytest
from conftest import load_solution
sol = load_solution("P7")

def test_basic_topk():
    assert sol.stable_topk([3,1,2,3,1], 2) == [3,3]

def test_stability_with_key():
    items = [("a",2),("b",1),("c",2)]
    assert sol.stable_topk(items, 2, key=lambda x: x[1]) == [("a",2),("c",2)]

def test_stability_equal_keys_order():
    items = [("x",5),("y",5),("z",5)]
    assert sol.stable_topk(items, 3, key=lambda x: x[1]) == [("x",5),("y",5),("z",5)]

def test_k_zero_or_negative():
    assert sol.stable_topk([1,2,3], 0) == []
    assert sol.stable_topk([1,2,3], -1) == []

def test_k_larger_than_list():
    assert sol.stable_topk([1,3,2], 10) == [3,2,1]

def test_no_mutation():
    data = [3,1,2]
    sol.stable_topk(data, 2)
    assert data == [3,1,2]

def test_incomparable_raises():
    with pytest.raises(TypeError):
        sol.stable_topk([1, "a", 2], 2)

def test_descending_order():
    assert sol.stable_topk([5,3,9,1,7], 3) == [9,7,5]
