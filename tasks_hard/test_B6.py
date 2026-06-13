# -*- coding: utf-8 -*-
from conftest import load_solution
sol = load_solution("B6")

def test_start_returns_first_q():
    q = sol.Quiz()
    assert q.start(1, now=0) == "Столица Франции?"

def test_correct_answer_scores():
    q = sol.Quiz()
    q.start(1, now=0)
    r = q.answer(1, "Париж", now=1)   # регистр игнор
    assert r["correct"] is True
    assert r["score"] == 1
    assert r["next_question"] == "2+2?"
    assert r["finished"] is False

def test_wrong_answer_advances_no_score():
    q = sol.Quiz()
    q.start(1, now=0)
    r = q.answer(1, "Лондон", now=1)
    assert r["correct"] is False
    assert r["score"] == 0
    assert r["next_question"] == "2+2?"

def test_timeout_not_counted():
    q = sol.Quiz(time_limit=30)
    q.start(1, now=0)
    r = q.answer(1, "Париж", now=100)   # верный текст, но таймаут
    assert r["timed_out"] is True
    assert r["correct"] is False
    assert r["score"] == 0

def test_full_run_finishes():
    q = sol.Quiz()
    q.start(1, now=0)
    q.answer(1, "париж", now=1)
    q.answer(1, "4", now=2)
    r = q.answer(1, "голубой", now=3)
    assert r["finished"] is True
    assert r["next_question"] is None
    assert r["score"] == 3

def test_answer_after_finish():
    q = sol.Quiz()
    q.start(1, now=0)
    for t in (1, 2, 3):
        q.answer(1, "x", now=t)
    r = q.answer(1, "x", now=4)
    assert r["finished"] is True
    assert r["next_question"] is None

def test_answer_without_start():
    q = sol.Quiz()
    r = q.answer(999, "париж", now=0)
    assert r["finished"] is True

def test_players_independent():
    q = sol.Quiz()
    q.start(1, now=0)
    q.start(2, now=0)
    q.answer(1, "париж", now=1)
    assert q.score(1) == 1
    assert q.score(2) == 0

def test_timer_resets_per_question():
    q = sol.Quiz(time_limit=30)
    q.start(1, now=0)
    q.answer(1, "париж", now=10)        # ok, время выдачи q2 = 10
    r = q.answer(1, "4", now=35)         # 35-10=25 <30 -> не таймаут
    assert r["timed_out"] is False
    assert r["correct"] is True
