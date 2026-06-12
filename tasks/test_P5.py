# -*- coding: utf-8 -*-
"""Тесты задачи P5: RateLimiter (скользящее окно)."""
import pytest
from conftest import load_solution

sol = load_solution("P5")


def test_allows_up_to_limit():
    rl = sol.RateLimiter(max_calls=3, window_seconds=10)
    assert rl.allow("u1", now=0.0) is True
    assert rl.allow("u1", now=1.0) is True
    assert rl.allow("u1", now=2.0) is True
    assert rl.allow("u1", now=3.0) is False


def test_window_slides():
    rl = sol.RateLimiter(max_calls=2, window_seconds=10)
    assert rl.allow("u1", now=0.0) is True
    assert rl.allow("u1", now=1.0) is True
    assert rl.allow("u1", now=5.0) is False
    assert rl.allow("u1", now=12.0) is True  # запись t=0 вышла из окна


def test_denied_attempt_not_counted():
    rl = sol.RateLimiter(max_calls=1, window_seconds=10)
    assert rl.allow("u1", now=0.0) is True
    for t in (1.0, 2.0, 3.0):
        assert rl.allow("u1", now=t) is False
    # отказы не записывались: после выхода t=0 из окна снова можно
    assert rl.allow("u1", now=11.0) is True


def test_keys_independent():
    rl = sol.RateLimiter(max_calls=1, window_seconds=10)
    assert rl.allow("u1", now=0.0) is True
    assert rl.allow("u2", now=0.0) is True
    assert rl.allow("u1", now=1.0) is False


def test_remaining_and_reset():
    rl = sol.RateLimiter(max_calls=3, window_seconds=10)
    assert rl.remaining("u1", now=0.0) == 3
    rl.allow("u1", now=0.0)
    rl.allow("u1", now=1.0)
    assert rl.remaining("u1", now=2.0) == 1
    rl.reset("u1")
    assert rl.remaining("u1", now=2.0) == 3


def test_constructor_validation():
    with pytest.raises(ValueError):
        sol.RateLimiter(max_calls=0, window_seconds=10)
    with pytest.raises(ValueError):
        sol.RateLimiter(max_calls=5, window_seconds=0)
