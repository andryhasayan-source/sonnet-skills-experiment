# -*- coding: utf-8 -*-
"""Тесты задачи B1: эхо-бот на aiogram 3.x.

Обработчики тестируются БЕЗ сети и без токена — через мок объекта Message.
Это образец подхода для всех задач-ботов.
"""
import asyncio
from unittest.mock import AsyncMock, MagicMock

from conftest import load_solution

sol = load_solution("B1")


def make_message(text):
    """Фальшивый Message: answer — асинхронный мок, текст задаём сами."""
    msg = MagicMock()
    msg.text = text
    msg.answer = AsyncMock()
    return msg


def run(coro):
    return asyncio.run(coro)


def test_router_exists():
    from aiogram import Router
    assert isinstance(sol.router, Router)


def test_cmd_start_text():
    msg = make_message("/start")
    run(sol.cmd_start(msg))
    msg.answer.assert_awaited_once()
    sent = msg.answer.await_args.args[0]
    assert sent == "Привет! Я бот-помощник. Напиши /help для списка команд."


def test_cmd_help_text():
    msg = make_message("/help")
    run(sol.cmd_help(msg))
    sent = msg.answer.await_args.args[0]
    assert sent == "Доступные команды:\n/start — приветствие\n/help — эта справка"


def test_echo_repeats_text():
    msg = make_message("Привет, бот")
    run(sol.echo(msg))
    sent = msg.answer.await_args.args[0]
    assert sent == "Вы написали: Привет, бот"


def test_echo_non_text():
    msg = make_message(None)  # стикер/фото
    run(sol.echo(msg))
    sent = msg.answer.await_args.args[0]
    assert sent == "Я понимаю только текст."
