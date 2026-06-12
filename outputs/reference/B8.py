from aiogram import Router, BaseMiddleware
from aiogram.filters import Command

ADMINS = {111}
allowed_users = {111, 222}

class AccessMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if user is None:
            return None
        if user.id in allowed_users or user.id in ADMINS:
            return await handler(event, data)
        await event.answer("Доступ запрещён.")
        return None

def parse_user_id(text):
    if not isinstance(text, str):
        return None
    parts = text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        return None
    uid = int(parts[1])
    return uid if uid > 0 else None

router = Router()

@router.message(Command("allow"))
async def cmd_allow(message):
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
async def cmd_deny(message):
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
    pass
