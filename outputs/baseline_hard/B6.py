"""Telegram-бот: викторина с подсчётом очков и таймаутом ответа."""

import asyncio
import logging

QUESTIONS = [
    {"q": "Столица Франции?", "a": "париж"},
    {"q": "2+2?", "a": "4"},
    {"q": "Цвет неба?", "a": "голубой"},
]


class Quiz:
    def __init__(self, questions=QUESTIONS, time_limit=30.0):
        self.questions = questions
        self.time_limit = time_limit
        self.players = {}  # user_id -> {"index": int, "score": int, "issued_at": float}

    def start(self, user_id, now):
        self.players[user_id] = {"index": 0, "score": 0, "issued_at": now}
        return self.questions[0]["q"]

    def answer(self, user_id, text, now):
        state = self.players.get(user_id)
        if state is None or state["index"] >= len(self.questions):
            return {
                "correct": False,
                "timed_out": False,
                "finished": True,
                "next_question": None,
                "score": state["score"] if state else 0,
            }

        current = self.questions[state["index"]]
        timed_out = (now - state["issued_at"]) > self.time_limit
        correct = (not timed_out) and (text.strip().lower() == current["a"].strip().lower())

        if correct:
            state["score"] += 1

        state["index"] += 1
        finished = state["index"] >= len(self.questions)

        if finished:
            next_question = None
        else:
            next_question = self.questions[state["index"]]["q"]
            state["issued_at"] = now

        return {
            "correct": correct,
            "timed_out": timed_out,
            "finished": finished,
            "next_question": next_question,
            "score": state["score"],
        }

    def score(self, user_id):
        state = self.players.get(user_id)
        return state["score"] if state else 0


if __name__ == "__main__":
    from aiogram import Bot, Dispatcher, F
    from aiogram.filters import Command
    from aiogram.types import Message
    import time

    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    quiz = Quiz()

    @dp.message(Command("start_quiz"))
    async def cmd_start_quiz(message: Message):
        question = quiz.start(message.from_user.id, time.monotonic())
        await message.answer(f"Вопрос: {question}")

    @dp.message(F.text)
    async def handle_answer(message: Message):
        result = quiz.answer(message.from_user.id, message.text, time.monotonic())

        if result["finished"] and result["next_question"] is None and message.from_user.id not in quiz.players:
            return

        if result["timed_out"]:
            reply = "Время вышло!"
        elif result["correct"]:
            reply = "Правильно!"
        else:
            reply = "Неправильно."

        if result["finished"]:
            reply += f" Викторина окончена. Ваш счёт: {result['score']}/{len(quiz.questions)}"
        else:
            reply += f" Следующий вопрос: {result['next_question']}"

        await message.answer(reply)

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())