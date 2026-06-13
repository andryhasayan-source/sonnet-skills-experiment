import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

TRANSITIONS = {
    "new": {"paid", "cancelled"},
    "paid": {"shipped", "refunded"},
    "shipped": {"delivered"},
    "delivered": set(),
    "cancelled": set(),
    "refunded": set(),
}


class OrderFSM:
    def __init__(self):
        self._orders: dict[str, list[str]] = {}

    def _ensure(self, order_id):
        if order_id not in self._orders:
            self._orders[order_id] = ["new"]

    def status(self, order_id) -> str:
        self._ensure(order_id)
        return self._orders[order_id][-1]

    def can_transition(self, order_id, to_status) -> bool:
        current = self.status(order_id)
        return to_status in TRANSITIONS.get(current, set())

    def transition(self, order_id, to_status) -> bool:
        if not self.can_transition(order_id, to_status):
            return False
        self._orders[order_id].append(to_status)
        return True

    def history(self, order_id) -> list:
        self._ensure(order_id)
        return list(self._orders[order_id])

    def is_terminal(self, order_id) -> bool:
        current = self.status(order_id)
        return len(TRANSITIONS.get(current, set())) == 0


router = Router()
fsm = OrderFSM()


@router.message(Command("status"))
async def cmd_status(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /status <order_id>")
        return
    order_id = parts[1].strip()
    await message.answer(f"Заказ {order_id}: статус = {fsm.status(order_id)}")


@router.message(Command("transition"))
async def cmd_transition(message: Message):
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Использование: /transition <order_id> <new_status>")
        return
    _, order_id, to_status = parts
    if to_status not in TRANSITIONS:
        await message.answer(f"Неизвестный статус: {to_status}")
        return
    if fsm.transition(order_id, to_status):
        await message.answer(f"Заказ {order_id} переведён в статус {to_status}")
    else:
        await message.answer(
            f"Невозможен переход из {fsm.status(order_id)} в {to_status}"
        )


@router.message(Command("history"))
async def cmd_history(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /history <order_id>")
        return
    order_id = parts[1].strip()
    await message.answer(f"История заказа {order_id}: {fsm.history(order_id)}")


@router.message(Command("is_terminal"))
async def cmd_is_terminal(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /is_terminal <order_id>")
        return
    order_id = parts[1].strip()
    await message.answer(
        f"Заказ {order_id} в терминальном статусе: {fsm.is_terminal(order_id)}"
    )


async def main():
    bot = Bot(token="YOUR_BOT_TOKEN")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())