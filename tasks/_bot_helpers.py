# -*- coding: utf-8 -*-
"""Общие помощники для тестов бот-задач."""
import asyncio
from unittest.mock import AsyncMock, MagicMock


def make_message(text, user_id=1):
    msg = MagicMock()
    msg.text = text
    msg.from_user = MagicMock()
    msg.from_user.id = user_id
    msg.answer = AsyncMock()
    return msg


def make_state(data=None):
    state = MagicMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()
    state.clear = AsyncMock()
    state.get_data = AsyncMock(return_value=data or {})
    return state


def sent_text(msg):
    """Текст последнего message.answer(...)."""
    args, kwargs = msg.answer.await_args
    return args[0] if args else kwargs.get("text")


def sent_markup(msg):
    args, kwargs = msg.answer.await_args
    if "reply_markup" in kwargs:
        return kwargs["reply_markup"]
    return args[1] if len(args) > 1 else None


def run(coro):
    return asyncio.run(coro)
