"""Брокер-распределитель заявок между операторами с балансировкой нагрузки."""

import asyncio
import logging

from aiogram import Bot, Dispatcher as AiogramDispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message


class Dispatcher:
    """Распределяет заявки между операторами по принципу наименьшей загрузки."""

    def __init__(self) -> None:
        # порядок добавления операторов важен для tie-break
        self._operators_order: list[int] = []
        self._loads: dict[int, int] = {}
        # ticket_id -> op_id для активных заявок
        self._tickets: dict[int, int] = {}
        # op_id -> set(ticket_id) активных заявок
        self._op_tickets: dict[int, set[int]] = {}

    def add_operator(self, op_id: int) -> None:
        if op_id in self._loads:
            return
        self._operators_order.append(op_id)
        self._loads[op_id] = 0
        self._op_tickets[op_id] = set()

    def remove_operator(self, op_id: int) -> list:
        if op_id not in self._loads:
            return []

        tickets = list(self._op_tickets[op_id])
        for t_id in tickets:
            del self._tickets[t_id]

        self._operators_order.remove(op_id)
        del self._loads[op_id]
        del self._op_tickets[op_id]

        return tickets

    def assign(self, ticket_id: int) -> int | None:
        if ticket_id in self._tickets:
            return self._tickets[ticket_id]

        if not self._operators_order:
            return None

        # выбираем оператора с минимальной загрузкой,
        # при равенстве — кто раньше добавлен (порядок в _operators_order)
        best_op = min(self._operators_order, key=lambda op: self._loads[op])

        self._tickets[ticket_id] = best_op
        self._op_tickets[best_op].add(ticket_id)
        self._loads[best_op] += 1

        return best_op

    def close(self, ticket_id: int) -> bool:
        if ticket_id not in self._tickets:
            return False

        op_id = self._tickets.pop(ticket_id)
        self._op_tickets[op_id].discard(ticket_id)
        self._loads[op_id] -= 1

        return True

    def load(self, op_id: int) -> int:
        return self._loads.get(op_id, 0)


router = Router()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token="YOUR_BOT_TOKEN")
    dp = AiogramDispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())