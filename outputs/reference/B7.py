from aiogram import Router
from aiogram.filters import Command

router = Router()

class TodoStorage:
    def __init__(self):
        self._items = {}

    def add(self, user_id, text):
        self._items.setdefault(user_id, []).append(text)
        return len(self._items[user_id])

    def list(self, user_id):
        return list(self._items.get(user_id, []))

    def done(self, user_id, number):
        items = self._items.get(user_id, [])
        if 1 <= number <= len(items):
            items.pop(number - 1)
            return True
        return False

storage = TodoStorage()

def format_list(items):
    if not items:
        return "Список пуст."
    lines = ["Ваши дела:"]
    for i, item in enumerate(items, 1):
        lines.append(f"{i}. {item}")
    return "\n".join(lines)

@router.message(Command("add"))
async def cmd_add(message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await message.answer("Использование: /add текст дела")
        return
    n = storage.add(message.from_user.id, parts[1].strip())
    await message.answer(f"Добавлено под номером {n}")

@router.message(Command("list"))
async def cmd_list(message):
    await message.answer(format_list(storage.list(message.from_user.id)))

@router.message(Command("done"))
async def cmd_done(message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip().lstrip("-").isdigit():
        await message.answer("Использование: /done номер")
        return
    number = int(parts[1].strip())
    if storage.done(message.from_user.id, number):
        await message.answer(f"Дело {number} выполнено!")
    else:
        await message.answer("Нет дела с таким номером.")

if __name__ == "__main__":
    pass
