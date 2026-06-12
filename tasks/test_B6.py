# -*- coding: utf-8 -*-
"""Тесты задачи B6: игра "Угадай число"."""
from unittest.mock import MagicMock

from conftest import load_solution
from _bot_helpers import make_message, sent_text, run

sol = load_solution("B6")


def fixed_rng(value):
    rng = MagicMock()
    rng.randint = MagicMock(return_value=value)
    return rng


def test_start_game_stores_number():
    n = sol.start_game(100, rng=fixed_rng(7))
    assert n == 7
    assert sol.games[100] == 7


def test_check_guess_flow():
    sol.start_game(200, rng=fixed_rng(5))
    assert sol.check_guess(200, 8) == "Меньше!"
    assert sol.check_guess(200, 2) == "Больше!"
    assert sol.check_guess(200, 5) == "Угадали!"
    assert 200 not in sol.games  # игра завершена


def test_check_guess_not_started():
    assert sol.check_guess(999999, 5) == "Игра не начата. Напишите /game"


def test_cmd_game_message():
    msg = make_message("/game", user_id=300)
    run(sol.cmd_game(msg))
    assert sent_text(msg) == "Я загадал число от 1 до 10. Угадай!"
    assert 300 in sol.games


def test_handle_guess_not_a_number():
    msg = make_message("привет", user_id=400)
    run(sol.handle_guess(msg))
    assert sent_text(msg) == "Отправьте число от 1 до 10."


def test_handle_guess_number():
    sol.games[500] = 5
    msg = make_message("8", user_id=500)
    run(sol.handle_guess(msg))
    assert sent_text(msg) == "Меньше!"
