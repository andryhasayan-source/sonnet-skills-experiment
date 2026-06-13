import logging
from aiogram import Bot, Dispatcher, Router, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, TelegramObject

ADMINS = {111}
allowed_users = {111, 222}

router = Router()


class AccessMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        user = getattr(event, "from_user", None)
        if user is None:
            return None
        if user.id in allowed_users or user.id in ADMINS:
            return await handler(event, data)
        await event.answer("Доступ запрещён.")
        return None


def parse_user_id(text: str) -> int | None:
    parts = text.strip().split()
    if len(parts) != 2:
        return None
    try:
        uid = int(parts[1])
    except ValueError:
        return None
    if uid <= 0:
        return None
    return uid


@router.message(Command("allow"))
async def cmd_allow(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Команда только для админов.")
        return
    uid = parse_user_id(message.text)
    if uid is None:
        await message.answer("Использование: /allow ID")
        return
    allowed_users.add(uid)
    await message.answer(f"Пользователь {uid} допущен.")


@router.message(Command("deny"))
async def cmd_deny(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Команда только для админов.")
        return
    uid = parse_user_id(message.text)
    if uid is None:
        await message.answer("Использование: /deny ID")
        return
    if uid in ADMINS:
        await message.answer("Нельзя заблокировать админа.")
        return
    allowed_users.discard(uid)
    await message.answer(f"Пользователь {uid} заблокирован.")


if __name__ == "__main__":
    import asyncio

    async def main():
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.message.middleware(AccessMiddleware())
        dp.include_router(router)
        await dp.start_polling(bot)

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())