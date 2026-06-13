# -*- coding: utf-8 -*-
import pytest
from conftest import load_solution
sol = load_solution("P8")

def test_starts_full():
    b = sol.TokenBucket(capacity=10, refill_rate=1)
    assert b.available(now=0) == 10

def test_consume_basic():
    b = sol.TokenBucket(capacity=10, refill_rate=1)
    assert b.consume(4, now=0) is True
    assert b.available(now=0) == pytest.approx(6)

def test_refill_over_time():
    b = sol.TokenBucket(capacity=10, refill_rate=2)
    b.consume(10, now=0)            # опустошили
    assert b.consume(1, now=0) is False
    assert b.consume(4, now=2) is True   # за 2с пришло 4 токена
    assert b.available(now=2) == pytest.approx(0)

def test_refill_capped():
    b = sol.TokenBucket(capacity=10, refill_rate=5)
    b.consume(10, now=0)
    assert b.available(now=1000) == 10   # не выше capacity

def test_request_over_capacity_false():
    b = sol.TokenBucket(capacity=5, refill_rate=1)
    assert b.consume(6, now=0) is False
    assert b.available(now=0) == 5       # не списано

def test_epsilon_tolerance():
    b = sol.TokenBucket(capacity=1, refill_rate=1)
    b.consume(1, now=0)
    # за ровно 1с накопился ровно 1 токен — должно хватить, несмотря на float
    assert b.consume(1, now=1) is True

def test_errors():
    with pytest.raises(ValueError):
        sol.TokenBucket(capacity=0, refill_rate=1)
    with pytest.raises(ValueError):
        sol.TokenBucket(capacity=5, refill_rate=-1)
    b = sol.TokenBucket(capacity=5, refill_rate=1)
    with pytest.raises(ValueError):
        b.consume(0, now=0)
