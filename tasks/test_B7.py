# -*- coding: utf-8 -*-
"""Тесты задачи B7: todo-бот."""
from conftest import load_solution
from _bot_helpers import make_message, sent_text, run

sol = load_solution("B7")


def test_storage_add_list_done():
    st = sol.TodoStorage()
    assert st.add(1, "хлеб") == 1
    assert st.add(1, "молоко") == 2
    assert st.list(1) == ["хлеб", "молоко"]
    assert st.done(1, 1) is True
    assert st.list(1) == ["молоко"]      # номера сдвинулись
    assert st.done(1, 5) is False


def test_storage_users_independent():
    st = sol.TodoStorage()
    st.add(1, "дело А")
    st.add(2, "дело Б")
    assert st.list(1) == ["дело А"]
    assert st.list(2) == ["дело Б"]


def test_format_list():
    assert sol.format_list([]) == "Список пуст."
    out = sol.format_list(["хлеб", "молоко"])
    assert out == "Ваши дела:\n1. хлеб\n2. молоко"


def test_cmd_add_ok():
    msg = make_message("/add купить хлеб", user_id=7001)
    run(sol.cmd_add(msg))
    assert sent_text(msg) == "Добавлено под номером 1"


def test_cmd_add_no_text():
    msg = make_message("/add", user_id=7002)
    run(sol.cmd_add(msg))
    assert sent_text(msg) == "Использование: /add текст дела"


def test_cmd_list_and_done():
    uid = 7003
    msg = make_message("/add позвонить клиенту", user_id=uid)
    run(sol.cmd_add(msg))

    msg = make_message("/list", user_id=uid)
    run(sol.cmd_list(msg))
    assert sent_text(msg) == "Ваши дела:\n1. позвонить клиенту"

    msg = make_message("/done 1", user_id=uid)
    run(sol.cmd_done(msg))
    assert sent_text(msg) == "Дело 1 выполнено!"

    msg = make_message("/done 1", user_id=uid)
    run(sol.cmd_done(msg))
    assert sent_text(msg) == "Нет дела с таким номером."

    msg = make_message("/done abc", user_id=uid)
    run(sol.cmd_done(msg))
    assert sent_text(msg) == "Использование: /done номер"
