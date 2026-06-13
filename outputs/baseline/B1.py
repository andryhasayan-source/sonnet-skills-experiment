from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот-помощник. Напиши /help для списка команд.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Доступные команды:\n/start — приветствие\n/help — эта справка")


@router.message()
async def echo(message: Message):
    if message.text is None:
        await message.answer("Я понимаю только текст.")
    else:
        await message.answer(f"Вы написали: {message.text}")


if __name__ == "__main__":
    import asyncio
    from aiogram import Bot, Dispatcher

    async def main():
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())