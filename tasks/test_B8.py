# -*- coding: utf-8 -*-
"""Тесты задачи B8: контроль доступа."""
from unittest.mock import AsyncMock, MagicMock

from conftest import load_solution
from _bot_helpers import make_message, sent_text, run

sol = load_solution("B8")

ADMIN_ID = 111
ALLOWED_ID = 222


def make_event(user_id):
    ev = MagicMock()
    if user_id is None:
        ev.from_user = None
    else:
        ev.from_user = MagicMock()
        ev.from_user.id = user_id
    ev.answer = AsyncMock()
    return ev


def test_parse_user_id():
    assert sol.parse_user_id("/allow 12345") == 12345
    assert sol.parse_user_id("/allow") is None
    assert sol.parse_user_id("/allow abc") is None


def test_middleware_allows_listed():
    mw = sol.AccessMiddleware()
    handler = AsyncMock(return_value="ok")
    assert run(mw(handler, make_event(ALLOWED_ID), {})) == "ok"
    assert run(mw(handler, make_event(ADMIN_ID), {})) == "ok"


def test_middleware_blocks_stranger():
    mw = sol.AccessMiddleware()
    handler = AsyncMock()
    ev = make_event(999888)
    assert run(mw(handler, ev, {})) is None
    ev.answer.assert_awaited_with("Доступ запрещён.")
    handler.assert_not_awaited()


def test_middleware_no_user_blocked():
    mw = sol.AccessMiddleware()
    handler = AsyncMock()
    assert run(mw(handler, make_event(None), {})) is None
    handler.assert_not_awaited()


def test_cmd_allow_admin_only():
    msg = make_message("/allow 333", user_id=ALLOWED_ID)  # не админ
    run(sol.cmd_allow(msg))
    assert sent_text(msg) == "Команда только для админов."

    msg = make_message("/allow 333", user_id=ADMIN_ID)
    run(sol.cmd_allow(msg))
    assert sent_text(msg) == "Пользователь 333 допущен."
    assert 333 in sol.allowed_users


def test_cmd_allow_bad_args():
    msg = make_message("/allow", user_id=ADMIN_ID)
    run(sol.cmd_allow(msg))
    assert sent_text(msg) == "Использование: /allow ID"


def test_cmd_deny():
    sol.allowed_users.add(444)
    msg = make_message("/deny 444", user_id=ADMIN_ID)
    run(sol.cmd_deny(msg))
    assert sent_text(msg) == "Пользователь 444 заблокирован."
    assert 444 not in sol.allowed_users

    # идемпотентность: повторный deny того же ID — тот же ответ
    msg = make_message("/deny 444", user_id=ADMIN_ID)
    run(sol.cmd_deny(msg))
    assert sent_text(msg) == "Пользователь 444 заблокирован."


def test_cmd_deny_admin_protected():
    msg = make_message(f"/deny {ADMIN_ID}", user_id=ADMIN_ID)
    run(sol.cmd_deny(msg))
    assert sent_text(msg) == "Нельзя заблокировать админа."
    assert ADMIN_ID in sol.allowed_users or ADMIN_ID in sol.ADMINS
