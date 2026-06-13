"""Многошаговый опрос (FSM) для aiogram 3.x с поддержкой /back."""

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
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
    """Возвращает None, если значение валидно, иначе текст ошибки."""
    if field == "age":
        text = value.strip()
        try:
            num = int(text)
        except ValueError:
            return "Возраст должен быть числом от 1 до 120."
        if num < 1 or num > 120:
            return "Возраст должен быть числом от 1 до 120."
        return None

    if field == "city":
        if len(value.strip()) < 2:
            return "Город слишком короткий."
        return None

    if field == "email":
        if value.count("@") != 1:
            return "Некорректный email."
        local, domain = value.split("@")
        if not local or not domain:
            return "Некорректный email."
        if "." not in domain:
            return "Некорректный email."
        return None

    return "Неизвестное поле."


async def cmd_survey(message: Message, state: FSMContext) -> None:
    await state.set_state(Survey.age)
    await state.update_data(step="age")
    await message.answer(QUESTIONS["age"])


async def cmd_back(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    current_step = data.get("step", ORDER[0])

    if current_step == ORDER[0]:
        await message.answer("Вы на первом вопросе.")
        return

    idx = ORDER.index(current_step)
    prev_step = ORDER[idx - 1]

    prev_state = getattr(Survey, prev_step)
    await state.set_state(prev_state)
    await state.update_data(step=prev_step)
    await message.answer(QUESTIONS[prev_step])


async def process_age(message: Message, state: FSMContext) -> None:
    if (message.text or "").strip() == "/back":
        await cmd_back(message, state)
        return

    error = validate("age", message.text)
    if error is not None:
        await message.answer(error)
        return

    await state.update_data(age=message.text.strip())
    await state.set_state(Survey.city)
    await state.update_data(step="city")
    await message.answer(QUESTIONS["city"])


async def process_city(message: Message, state: FSMContext) -> None:
    if (message.text or "").strip() == "/back":
        await cmd_back(message, state)
        return

    error = validate("city", message.text)
    if error is not None:
        await message.answer(error)
        return

    await state.update_data(city=message.text.strip())
    await state.set_state(Survey.email)
    await state.update_data(step="email")
    await message.answer(QUESTIONS["email"])


async def process_email(message: Message, state: FSMContext) -> None:
    if (message.text or "").strip() == "/back":
        await cmd_back(message, state)
        return

    error = validate("email", message.text)
    if error is not None:
        await message.answer(error)
        return

    await state.update_data(email=message.text.strip())
    data = await state.get_data()

    await message.answer(
        f"Готово! Возраст: {data.get('age')}, город: {data.get('city')}, "
        f"email: {data.get('email')}"
    )
    await state.clear()


router.message.register(cmd_survey, Command("survey"))
router.message.register(cmd_back, Command("back"))
router.message.register(process_age, Survey.age)
router.message.register(process_city, Survey.city)
router.message.register(process_email, Survey.email)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def main() -> None:
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())