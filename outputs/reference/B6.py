import random
from aiogram import Router
from aiogram.filters import Command

router = Router()
games = {}

def start_game(user_id, rng=None):
    rng = rng or random
    number = rng.randint(1, 10)
    games[user_id] = number
    return number

def check_guess(user_id, guess):
    if user_id not in games:
        return "Игра не начата. Напишите /game"
    secret = games[user_id]
    if guess > secret:
        return "Меньше!"
    if guess < secret:
        return "Больше!"
    del games[user_id]
    return "Угадали!"

@router.message(Command("game"))
async def cmd_game(message):
    start_game(message.from_user.id)
    await message.answer("Я загадал число от 1 до 10. Угадай!")

@router.message()
async def handle_guess(message):
    text = (message.text or "").strip()
    try:
        guess = int(text)
    except (ValueError, TypeError):
        await message.answer("Отправьте число от 1 до 10.")
        return
    await message.answer(check_guess(message.from_user.id, guess))

if __name__ == "__main__":
    pass
