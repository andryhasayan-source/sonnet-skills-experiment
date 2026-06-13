# -*- coding: utf-8 -*-
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
    store = dict(data or {})
    state = MagicMock()
    state.set_state = AsyncMock()
    async def _update(**kw):
        store.update(kw)
    state.update_data = AsyncMock(side_effect=_update)
    state.clear = AsyncMock()
    async def _get():
        return dict(store)
    state.get_data = AsyncMock(side_effect=_get)
    state._store = store
    return state

def sent_text(msg):
    args, kwargs = msg.answer.await_args
    return args[0] if args else kwargs.get("text")

def run(coro):
    return asyncio.run(coro)
