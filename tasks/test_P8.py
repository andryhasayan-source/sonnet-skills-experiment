# -*- coding: utf-8 -*-
"""Тесты задачи P8: TTLCache."""
import pytest
from conftest import load_solution

sol = load_solution("P8")


def test_set_get():
    c = sol.TTLCache(max_size=10, ttl_seconds=60)
    c.set("a", 1, now=0)
    assert c.get("a", now=1) == 1
    assert c.get("nope", now=1) is None


def test_ttl_expiry():
    c = sol.TTLCache(max_size=10, ttl_seconds=10)
    c.set("a", 1, now=0)
    assert c.get("a", now=5) == 1
    assert c.get("a", now=15) is None  # протух


def test_lru_eviction():
    c = sol.TTLCache(max_size=2, ttl_seconds=100)
    c.set("a", 1, now=0)
    c.set("b", 2, now=1)
    c.get("a", now=2)        # a становится свежеиспользованным
    c.set("c", 3, now=3)     # вытесняется b, а не a
    assert c.get("a", now=4) == 1
    assert c.get("b", now=4) is None
    assert c.get("c", now=4) == 3


def test_len_counts_alive_only():
    c = sol.TTLCache(max_size=10, ttl_seconds=0.05)
    c.set("a", 1)
    assert len(c) == 1
    import time
    time.sleep(0.08)
    assert len(c) == 0


def test_constructor_validation():
    with pytest.raises(ValueError):
        sol.TTLCache(max_size=0, ttl_seconds=10)
    with pytest.raises(ValueError):
        sol.TTLCache(max_size=5, ttl_seconds=0)
