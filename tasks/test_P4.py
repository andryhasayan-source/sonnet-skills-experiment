# -*- coding: utf-8 -*-
"""Тесты задачи P4: декоратор retry."""
import pytest
from conftest import load_solution

sol = load_solution("P4")


def test_success_no_extra_calls():
    calls = {"n": 0}

    @sol.retry(times=3, delay=0)
    def ok():
        calls["n"] += 1
        return 42

    assert ok() == 42
    assert calls["n"] == 1  # при успехе лишних попыток нет


def test_retries_then_succeeds():
    calls = {"n": 0}

    @sol.retry(times=3, delay=0, exceptions=(ConnectionError,))
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("boom")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3


def test_raises_after_all_attempts():
    calls = {"n": 0}

    @sol.retry(times=3, delay=0, exceptions=(ValueError,))
    def always_fails():
        calls["n"] += 1
        raise ValueError("nope")

    with pytest.raises(ValueError):
        always_fails()
    assert calls["n"] == 3


def test_unlisted_exception_not_retried():
    calls = {"n": 0}

    @sol.retry(times=5, delay=0, exceptions=(ConnectionError,))
    def wrong_error():
        calls["n"] += 1
        raise KeyError("other")

    with pytest.raises(KeyError):
        wrong_error()
    assert calls["n"] == 1  # чужое исключение пролетает сразу


def test_wraps_preserves_metadata():
    @sol.retry(times=2, delay=0)
    def documented():
        """my doc"""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "my doc"


def test_invalid_times():
    with pytest.raises(ValueError):
        sol.retry(times=0, delay=0)
