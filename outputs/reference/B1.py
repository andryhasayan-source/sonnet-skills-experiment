from aiogram import Router, F
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message):
    await message.answer("Привет! Я бот-помощник. Напиши /help для списка команд.")

@router.message(Command("help"))
async def cmd_help(message):
    await message.answer("Доступные команды:\n/start — приветствие\n/help — эта справка")

@router.message()
async def echo(message):
    if message.text is None:
        await message.answer("Я понимаю только текст.")
    else:
        await message.answer(f"Вы написали: {message.text}")

if __name__ == "__main__":
    pass
