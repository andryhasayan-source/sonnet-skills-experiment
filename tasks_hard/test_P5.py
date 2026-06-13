# -*- coding: utf-8 -*-
import pytest
from conftest import load_solution
sol = load_solution("P5")

def test_first_not_duplicate():
    d = sol.EventDeduplicator(window_seconds=10)
    assert d.is_duplicate("e1", now=0) is False

def test_duplicate_within_window():
    d = sol.EventDeduplicator(window_seconds=10)
    d.is_duplicate("e1", now=0)
    assert d.is_duplicate("e1", now=5) is True

def test_expired_not_duplicate():
    d = sol.EventDeduplicator(window_seconds=10)
    d.is_duplicate("e1", now=0)
    assert d.is_duplicate("e1", now=10) is False   # ровно окно -> протухло

def test_repeat_refreshes_window():
    d = sol.EventDeduplicator(window_seconds=10)
    d.is_duplicate("e1", now=0)
    assert d.is_duplicate("e1", now=8) is True      # обновили до 8
    assert d.is_duplicate("e1", now=17) is True      # 17-8 < 10, ещё жив
    assert d.is_duplicate("e1", now=27) is False     # 27-17 ==10 -> протух

def test_active_count():
    d = sol.EventDeduplicator(window_seconds=10)
    d.is_duplicate("a", now=0)
    d.is_duplicate("b", now=1)
    assert d.active_count(now=2) == 2
    # now=10: a (t=0) протух (10-0>=10), b (t=1) жив (10-1=9<10)
    assert d.active_count(now=10) == 1

def test_purge_returns_count():
    d = sol.EventDeduplicator(window_seconds=10)
    d.is_duplicate("a", now=0)
    d.is_duplicate("b", now=1)
    # now=10: протухает только a -> удалено 1, остаётся b
    assert d.purge(now=10) == 1
    assert d.active_count(now=10) == 1

def test_invalid_window():
    with pytest.raises(ValueError):
        sol.EventDeduplicator(window_seconds=0)
