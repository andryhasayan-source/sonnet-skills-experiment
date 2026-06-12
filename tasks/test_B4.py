# -*- coding: utf-8 -*-
"""Тесты задачи B4: пагинация каталога."""
from unittest.mock import AsyncMock, MagicMock

from aiogram.types import InlineKeyboardMarkup

from conftest import load_solution
from _bot_helpers import run

sol = load_solution("B4")


def buttons(kb):
    return [b for row in kb.inline_keyboard for b in row]


def test_items_and_pages():
    assert len(sol.ITEMS) == 23
    assert sol.total_pages(sol.ITEMS) == 5
    assert sol.total_pages([]) == 0


def test_get_page():
    assert sol.get_page(sol.ITEMS, 0) == sol.ITEMS[:5]
    assert sol.get_page(sol.ITEMS, 4) == sol.ITEMS[20:]   # хвост из 3
    assert sol.get_page(sol.ITEMS, 99) == []


def test_build_page_text():
    text = sol.build_page_text(sol.ITEMS, 1)
    assert text.startswith("Страница 2/5:")
    assert f"- {sol.ITEMS[5]}" in text
    assert f"- {sol.ITEMS[9]}" in text
    assert f"- {sol.ITEMS[10]}" not in text


def test_keyboard_first_middle_last():
    kb0 = sol.build_pager_keyboard(0, 5)
    texts0 = [b.text for b in buttons(kb0)]
    assert ">>" in texts0 and "<<" not in texts0

    kb2 = sol.build_pager_keyboard(2, 5)
    data2 = {b.text: b.callback_data for b in buttons(kb2)}
    assert data2["<<"] == "page:1"
    assert data2[">>"] == "page:3"

    kb4 = sol.build_pager_keyboard(4, 5)
    texts4 = [b.text for b in buttons(kb4)]
    assert "<<" in texts4 and ">>" not in texts4


def test_on_page_edits_message():
    callback = MagicMock()
    callback.data = "page:2"
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.answer = AsyncMock()
    run(sol.on_page(callback))
    callback.message.edit_text.assert_awaited()
    callback.answer.assert_awaited()
    args, kwargs = callback.message.edit_text.await_args
    text = args[0] if args else kwargs.get("text")
    assert text.startswith("Страница 3/5:")
