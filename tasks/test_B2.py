# -*- coding: utf-8 -*-
"""Тесты задачи B2: меню кафе."""
from aiogram.types import ReplyKeyboardMarkup

from conftest import load_solution
from _bot_helpers import make_message, sent_text, sent_markup, run

sol = load_solution("B2")


def keyboard_texts(kb):
    return [[btn.text for btn in row] for row in kb.keyboard]


def test_menu_constant():
    assert sol.MENU == {"Кофе": 150, "Чай": 100, "Десерт": 250}


def test_keyboard_structure():
    kb = sol.build_menu_keyboard()
    assert isinstance(kb, ReplyKeyboardMarkup)
    assert kb.resize_keyboard is True
    flat = [t for row in keyboard_texts(kb) for t in row]
    for name in sol.MENU:
        assert name in flat
    assert "Корзина" in flat
    # "Корзина" отдельной строкой
    assert ["Корзина"] in keyboard_texts(kb)


def test_cmd_start_sends_keyboard():
    msg = make_message("/start")
    run(sol.cmd_start(msg))
    assert sent_text(msg) == "Добро пожаловать! Выберите позицию:"
    assert isinstance(sent_markup(msg), ReplyKeyboardMarkup)


def test_handle_menu_choice():
    msg = make_message("Кофе")
    run(sol.handle_menu_choice(msg))
    assert sent_text(msg) == "Кофе — 150 руб. Добавлено в заказ."


def test_format_price():
    assert sol.format_price("Чай") == "Чай — 100 руб."
    assert sol.format_price("Борщ") == "Нет такой позиции"
