# -*- coding: utf-8 -*-
"""Тесты задачи B5: антифлуд-middleware."""
from unittest.mock import AsyncMock, MagicMock

from conftest import load_solution
from _bot_helpers import run

sol = load_solution("B5")


def test_storage_within_limit():
    st = sol.ThrottleStorage(limit=2, window=10)
    assert st.hit(1, now=0.0) is True
    assert st.hit(1, now=1.0) is True
    assert st.hit(1, now=2.0) is False


def test_storage_window_slides():
    st = sol.ThrottleStorage(limit=1, window=10)
    assert st.hit(1, now=0.0) is True
    assert st.hit(1, now=5.0) is False
    assert st.hit(1, now=12.0) is True


def test_storage_users_independent():
    st = sol.ThrottleStorage(limit=1, window=10)
    assert st.hit(1, now=0.0) is True
    assert st.hit(2, now=0.0) is True


def make_event(user_id):
    ev = MagicMock()
    if user_id is None:
        ev.from_user = None
    else:
        ev.from_user = MagicMock()
        ev.from_user.id = user_id
    ev.answer = AsyncMock()
    return ev


def test_middleware_passes_then_blocks():
    mw = sol.AntiFloodMiddleware(limit=2, window=60.0)
    handler = AsyncMock(return_value="handled")

    ev = make_event(42)
    assert run(mw(handler, ev, {})) == "handled"
    assert run(mw(handler, ev, {})) == "handled"
    result = run(mw(handler, ev, {}))
    assert result is None
    ev.answer.assert_awaited_with("Слишком часто! Подождите немного.")
    assert handler.await_count == 2  # третий раз обработчик не вызван


def test_middleware_no_user_passes():
    mw = sol.AntiFloodMiddleware(limit=1, window=60.0)
    handler = AsyncMock(return_value="ok")
    ev = make_event(None)
    assert run(mw(handler, ev, {})) == "ok"
    assert run(mw(handler, ev, {})) == "ok"  # без from_user лимит не применяется
