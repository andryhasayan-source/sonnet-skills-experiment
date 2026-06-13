import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


class TodoStorage:
    def __init__(self):
        self._data: dict[int, list[str]] = {}

    def add(self, user_id: int, text: str) -> int:
        items = self._data.setdefault(user_id, [])
        items.append(text)
        return len(items)

    def list(self, user_id: int) -> list[str]:
        return self._data.get(user_id, [])

    def done(self, user_id: int, number: int) -> bool:
        items = self._data.get(user_id, [])
        if 1 <= number <= len(items):
            items.pop(number - 1)
            return True
        return False


storage = TodoStorage()


def format_list(items: list[str]) -> str:
    if not items:
        return "Список пуст."
    return "Ваши дела:\n" + "\n".join(f"{i}. {t}" for i, t in enumerate(items, 1))


@router.message(Command("add"))
async def cmd_add(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await message.answer("Использование: /add текст дела")
        return
    n = storage.add(message.from_user.id, parts[1].strip())
    await message.answer(f"Добавлено под номером {n}")


@router.message(Command("list"))
async def cmd_list(message: Message):
    await message.answer(format_list(storage.list(message.from_user.id)))


@router.message(Command("done"))
async def cmd_done(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip().isdigit():
        await message.answer("Использование: /done номер")
        return
    number = int(parts[1].strip())
    if storage.done(message.from_user.id, number):
        await message.answer(f"Дело {number} выполнено!")
    else:
        await message.answer("Нет дела с таким номером.")


if __name__ == "__main__":
    async def main():
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())