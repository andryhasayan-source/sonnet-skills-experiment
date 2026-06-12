# -*- coding: utf-8 -*-
"""Тесты задачи B3: анкета через FSM."""
from conftest import load_solution
from _bot_helpers import make_message, make_state, sent_text, run

sol = load_solution("B3")


def test_states_exist():
    assert hasattr(sol.OrderForm, "name")
    assert hasattr(sol.OrderForm, "phone")


def test_cmd_order():
    msg, state = make_message("/order"), make_state()
    run(sol.cmd_order(msg, state))
    state.set_state.assert_awaited_with(sol.OrderForm.name)
    assert sent_text(msg) == "Как вас зовут?"


def test_process_name_too_short():
    msg, state = make_message("Я"), make_state()
    run(sol.process_name(msg, state))
    assert sent_text(msg) == "Имя слишком короткое, попробуйте ещё раз."
    state.set_state.assert_not_awaited()


def test_process_name_ok():
    msg, state = make_message("Иван"), make_state()
    run(sol.process_name(msg, state))
    state.update_data.assert_awaited()
    # имя попало в данные (kwargs или словарь первым аргументом)
    args, kwargs = state.update_data.await_args
    stored = kwargs.get("name") or (args[0].get("name") if args and isinstance(args[0], dict) else None)
    assert stored == "Иван"
    state.set_state.assert_awaited_with(sol.OrderForm.phone)
    assert sent_text(msg) == "Укажите телефон:"


def test_is_valid_phone():
    assert sol.is_valid_phone("8 905 123-45-67") is True
    assert sol.is_valid_phone("9051234567") is True
    assert sol.is_valid_phone("12345") is False


def test_process_phone_invalid():
    msg, state = make_message("12345"), make_state()
    run(sol.process_phone(msg, state))
    assert sent_text(msg) == "Телефон некорректен, попробуйте ещё раз."
    state.clear.assert_not_awaited()


def test_process_phone_ok():
    msg = make_message("89051234567")
    state = make_state(data={"name": "Иван"})
    run(sol.process_phone(msg, state))
    assert sent_text(msg) == "Спасибо, Иван! Заказ принят, мы перезвоним."
    state.clear.assert_awaited()
