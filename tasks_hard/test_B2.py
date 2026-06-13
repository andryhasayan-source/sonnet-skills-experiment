# -*- coding: utf-8 -*-
from conftest import load_solution
from _bot_helpers import make_message, make_state, sent_text, run
sol = load_solution("B2")

def test_validate_age():
    assert sol.validate("age", "30") is None
    assert sol.validate("age", "0") is not None
    assert sol.validate("age", "121") is not None
    assert sol.validate("age", "abc") is not None

def test_validate_city():
    assert sol.validate("city", "Москва") is None
    assert sol.validate("city", " a ") is not None

def test_validate_email():
    assert sol.validate("email", "a@b.ru") is None
    assert sol.validate("email", "ab.ru") is not None
    assert sol.validate("email", "a@@b.ru") is not None
    assert sol.validate("email", "a@bru") is not None

def test_cmd_survey_starts():
    msg, state = make_message("/survey"), make_state()
    run(sol.cmd_survey(msg, state))
    state.set_state.assert_awaited_with(sol.Survey.age)
    assert sent_text(msg) == "Ваш возраст?"

def test_process_age_invalid_stays():
    msg, state = make_message("999"), make_state({"_step": "age"})
    run(sol.process_age(msg, state))
    assert sent_text(msg) == "Возраст должен быть числом от 1 до 120."
    state.set_state.assert_not_awaited()

def test_process_age_ok_advances():
    msg, state = make_message("30"), make_state({"_step": "age"})
    run(sol.process_age(msg, state))
    state.set_state.assert_awaited_with(sol.Survey.city)
    assert sent_text(msg) == "Ваш город?"
    assert state._store.get("age") == "30"

def test_back_from_city():
    msg, state = make_message("/back"), make_state({"_step": "city", "age": "30"})
    run(sol.cmd_back(msg, state))
    state.set_state.assert_awaited_with(sol.Survey.age)
    assert sent_text(msg) == "Ваш возраст?"

def test_back_from_first():
    msg, state = make_message("/back"), make_state({"_step": "age"})
    run(sol.cmd_back(msg, state))
    assert sent_text(msg) == "Вы на первом вопросе."

def test_finish_after_email():
    state = make_state({"_step": "email", "age": "30", "city": "Москва"})
    msg = make_message("a@b.ru")
    run(sol.process_email(msg, state))
    assert "Готово!" in sent_text(msg)
    assert "30" in sent_text(msg) and "Москва" in sent_text(msg)
    state.clear.assert_awaited()
