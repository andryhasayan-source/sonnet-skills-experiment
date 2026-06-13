import random
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.enums import ContentType

router = Router()
games = {}


def start_game(user_id: int, rng=None) -> int:
    if rng is None:
        number = random.randint(1, 10)
    else:
        number = rng.randint(1, 10)
    games[user_id] = number
    return number


def check_guess(user_id: int, guess: int) -> str:
    if user_id not in games:
        return "Игра не начата. Напишите /game"

    number = games[user_id]

    if guess > number:
        return "Меньше!"
    elif guess < number:
        return "Больше!"
    else:
        del games[user_id]
        return "Угадали!"


@router.message(Command("game"))
async def cmd_game(message: Message):
    start_game(message.from_user.id)
    await message.answer("Я загадал число от 1 до 10. Угадай!")


@router.message()
async def handle_guess(message: Message):
    text = message.text or ""
    try:
        guess = int(text)
    except ValueError:
        await message.answer("Отправьте число от 1 до 10.")
        return

    result = check_guess(message.from_user.id, guess)
    await message.answer(result)


if __name__ == "__main__":
    import asyncio

    TOKEN = "YOUR_BOT_TOKEN"

    async def main():
        bot = Bot(token=TOKEN)
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())