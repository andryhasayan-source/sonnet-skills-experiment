"""
Многошаговый опрос (FSM) для Telegram-бота на aiogram 3.x.

Сценарий /survey:
    1) "Ваш возраст?"
    2) "Ваш город?"
    3) "Ваш email?"
    -> итоговое сообщение со всеми ответами.

В любой момент опроса команда /back возвращает на предыдущий шаг
и повторяет его вопрос. Если пользователь находится на первом шаге —
сообщается, что это первый вопрос, и шаг не меняется.
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message


router = Router()


class Survey(StatesGroup):
    age = State()
    city = State()
    email = State()


QUESTIONS = {
    "age": "Ваш возраст?",
    "city": "Ваш город?",
    "email": "Ваш email?",
}

ORDER = ["age", "city", "email"]


def validate(field: str, value: str) -> str | None:
    """
    Проверяет значение для конкретного поля опроса.

    Возвращает None, если значение валидно, иначе — текст ошибки.
    """
    if value is None:
        value = ""

    if field == "age":
        stripped = value.strip()
        try:
            age_value = int(stripped)
        except (ValueError, TypeError):
            return "Возраст должен быть числом от 1 до 120."
        if not (1 <= age_value <= 120):
            return "Возраст должен быть числом от 1 до 120."
        return None

    if field == "city":
        if len(value.strip()) < 2:
            return "Город слишком короткий."
        return None

    if field == "email":
        stripped = value.strip()
        if stripped.count("@") != 1:
            return "Некорректный email."
        local_part, domain_part = stripped.split("@")
        if not local_part or not domain_part:
            return "Некорректный email."
        if "." not in domain_part:
            return "Некорректный email."
        return None

    return None


async def cmd_survey(message: Message, state: FSMContext) -> None:
    """Старт опроса: переходим к первому шагу (age) и задаём вопрос."""
    await state.set_state(Survey.age)
    await state.update_data(step="age")
    await message.answer(QUESTIONS["age"])


async def cmd_back(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /back.

    Если текущий шаг — первый (age), сообщаем об этом и остаёмся на месте.
    Иначе переходим на предыдущий шаг и повторяем его вопрос.
    """
    data = await state.get_data()
    current_step = data.get("step")

    if current_step not in ORDER:
        # Пользователь не в опросе — ничего не делаем.
        return

    current_index = ORDER.index(current_step)

    if current_index == 0:
        await message.answer("Вы на первом вопросе.")
        return

    previous_step = ORDER[current_index - 1]
    await state.set_state(getattr(Survey, previous_step))
    await state.update_data(step=previous_step)
    await message.answer(QUESTIONS[previous_step])


async def _process_step(message: Message, state: FSMContext, field: str) -> None:
    """
    Общая логика обработки шага опроса.

    - Если пользователь отправил /back — делегируем в cmd_back (приоритет).
    - Если значение невалидно — показываем ошибку и остаёмся на шаге.
    - Если значение валидно — сохраняем его и переходим к следующему шагу
      (или завершаем опрос, если это был последний шаг).
    """
    text = message.text or ""

    if text == "/back":
        await cmd_back(message, state)
        return

    error = validate(field, text)
    if error is not None:
        await message.answer(error)
        return

    await state.update_data(**{field: text})

    current_index = ORDER.index(field)

    if current_index + 1 < len(ORDER):
        next_field = ORDER[current_index + 1]
        await state.set_state(getattr(Survey, next_field))
        await state.update_data(step=next_field)
        await message.answer(QUESTIONS[next_field])
    else:
        data = await state.get_data()
        await message.answer(
            "Готово! Возраст: {age}, город: {city}, email: {email}".format(
                age=data.get("age"),
                city=data.get("city"),
                email=data.get("email"),
            )
        )
        await state.clear()


@router.message(Command("survey"))
async def _on_cmd_survey(message: Message, state: FSMContext) -> None:
    await cmd_survey(message, state)


@router.message(Command("back"))
async def _on_cmd_back(message: Message, state: FSMContext) -> None:
    await cmd_back(message, state)


@router.message(StateFilter(Survey.age))
async def process_age(message: Message, state: FSMContext) -> None:
    await _process_step(message, state, "age")


@router.message(StateFilter(Survey.city))
async def process_city(message: Message, state: FSMContext) -> None:
    await _process_step(message, state, "city")


@router.message(StateFilter(Survey.email))
async def process_email(message: Message, state: FSMContext) -> None:
    await _process_step(message, state, "email")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    BOT_TOKEN = os.getenv("BOT_TOKEN", "")

    async def main() -> None:
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())