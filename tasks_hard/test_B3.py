# -*- coding: utf-8 -*-
import pytest
from unittest.mock import AsyncMock, MagicMock
from conftest import load_solution
from _bot_helpers import run
sol = load_solution("B3")

def test_pack_basic():
    assert sol.pack("view", 5, 2) == "act:view:5:2"
    assert sol.pack("edit", 1) == "act:edit:1:0"

def test_pack_invalid():
    for args in [("bad", 1, 0), ("view", 0, 0), ("view", -1, 0), ("view", 1, -1)]:
        with pytest.raises(ValueError):
            sol.pack(*args)

def test_roundtrip():
    for action in ("view", "edit", "del"):
        for eid in (1, 42, 9999):
            for page in (0, 3, 100):
                d = sol.parse(sol.pack(action, eid, page))
                assert d == {"action": action, "entity_id": eid, "page": page}

def test_parse_invalid():
    for bad in ["", "act:view:5", "act:view:5:2:7", "x:view:5:2",
                "act:fly:5:2", "act:view:0:2", "act:view:-5:2",
                "act:view:5:-1", "act:view:007:2", "act:view:abc:2",
                "act:view:5:2:", "act::5:2"]:
        assert sol.parse(bad) is None, bad

def test_on_action_valid():
    cb = MagicMock()
    cb.data = "act:edit:7:3"
    cb.answer = AsyncMock()
    cb.message = MagicMock()
    cb.message.answer = AsyncMock()
    run(sol.on_action(cb))
    cb.answer.assert_awaited_with()
    text = cb.message.answer.await_args.args[0]
    assert "edit" in text and "#7" in text and "3" in text

def test_on_action_invalid():
    cb = MagicMock()
    cb.data = "garbage"
    cb.answer = AsyncMock()
    cb.message = MagicMock()
    cb.message.answer = AsyncMock()
    run(sol.on_action(cb))
    cb.answer.assert_awaited_with("Некорректная кнопка", show_alert=True)
    cb.message.answer.assert_not_awaited()
