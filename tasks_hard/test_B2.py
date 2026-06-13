# -*- coding: utf-8 -*-
# Модель-независимая версия: состояние ведём через реальные обработчики,
# не угадывая имя внутреннего ключа решения.
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
    # сначала корректно стартуем опрос (решение само выставит своё состояние)
    state = make_state()
    run(sol.cmd_survey(make_message("/survey"), state))
    msg = make_message("999")
    run(sol.process_age(msg, state))
    assert sent_text(msg) == "Возраст должен быть числом от 1 до 120."

def test_process_age_ok_advances():
    state = make_state()
    run(sol.cmd_survey(make_message("/survey"), state))
    msg = make_message("30")
    run(sol.process_age(msg, state))
    state.set_state.assert_awaited_with(sol.Survey.city)
    assert sent_text(msg) == "Ваш город?"

def test_back_from_city():
    # реальный путь: старт -> ввели возраст -> на шаге city -> /back
    state = make_state()
    run(sol.cmd_survey(make_message("/survey"), state))
    run(sol.process_age(make_message("30"), state))   # теперь на city
    back = make_message("/back")
    run(sol.cmd_back(back, state))
    state.set_state.assert_awaited_with(sol.Survey.age)
    assert sent_text(back) == "Ваш возраст?"

def test_back_from_first():
    state = make_state()
    run(sol.cmd_survey(make_message("/survey"), state))   # на первом шаге
    back = make_message("/back")
    run(sol.cmd_back(back, state))
    assert sent_text(back) == "Вы на первом вопросе."

def test_finish_after_email():
    # проходим опрос целиком реальными шагами
    state = make_state()
    run(sol.cmd_survey(make_message("/survey"), state))
    run(sol.process_age(make_message("30"), state))
    run(sol.process_city(make_message("Москва"), state))
    msg = make_message("a@b.ru")
    run(sol.process_email(msg, state))
    assert "Готово!" in sent_text(msg)
    assert "30" in sent_text(msg) and "Москва" in sent_text(msg)
    state.clear.assert_awaited()
