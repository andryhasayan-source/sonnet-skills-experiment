# -*- coding: utf-8 -*-
from unittest.mock import AsyncMock, MagicMock
from conftest import load_solution
from _bot_helpers import run
sol = load_solution("B5")

def test_separate_counters():
    rl = sol.DualRateLimiter(cmd_limit=2, cmd_window=10, msg_limit=5, msg_window=10)
    # команды и сообщения независимы
    assert rl.check(1, True, now=0) is True
    assert rl.check(1, True, now=1) is True
    assert rl.check(1, True, now=2) is False        # лимит команд исчерпан
    assert rl.check(1, False, now=2) is True        # сообщения ещё свободны

def test_window_slides():
    rl = sol.DualRateLimiter(cmd_limit=1, cmd_window=10, msg_limit=1, msg_window=10)
    assert rl.check(1, True, now=0) is True
    assert rl.check(1, True, now=5) is False
    assert rl.check(1, True, now=11) is True        # старая команда вышла из окна

def test_rejected_not_counted():
    rl = sol.DualRateLimiter(cmd_limit=1, cmd_window=10, msg_limit=1, msg_window=10)
    assert rl.check(1, True, now=0) is True
    assert rl.check(1, True, now=1) is False
    assert rl.check(1, True, now=11) is True        # в окне только t=0

def test_users_independent():
    rl = sol.DualRateLimiter(cmd_limit=1, cmd_window=10, msg_limit=1, msg_window=10)
    assert rl.check(1, True, now=0) is True
    assert rl.check(2, True, now=0) is True

def _event(text, uid=1):
    ev = MagicMock()
    ev.from_user = MagicMock()
    ev.from_user.id = uid
    ev.text = text
    ev.answer = AsyncMock()
    return ev

def test_middleware_passes_within_limit():
    mw = sol.RateLimitMiddleware(cmd_limit=100, msg_limit=100)
    handler = AsyncMock(return_value="ok")
    assert run(mw(handler, _event("/start"), {})) == "ok"
    assert run(mw(handler, _event("hello"), {})) == "ok"

def test_middleware_no_user_passes():
    mw = sol.RateLimitMiddleware(cmd_limit=1, msg_limit=1)
    handler = AsyncMock(return_value="ok")
    ev = MagicMock()
    ev.from_user = None
    assert run(mw(handler, ev, {})) == "ok"

def test_middleware_blocks_over_limit():
    mw = sol.RateLimitMiddleware(cmd_limit=1, cmd_window=1000,
                                 msg_limit=1, msg_window=1000)
    handler = AsyncMock(return_value="ok")
    ev = _event("/a")
    assert run(mw(handler, ev, {})) == "ok"
    ev2 = _event("/b")
    assert run(mw(handler, ev2, {})) is None
    ev2.answer.assert_awaited_with("Лимит запросов исчерпан, подождите.")
