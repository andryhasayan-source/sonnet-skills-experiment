from collections import OrderedDict
from aiogram import Router

router = Router()


class Dispatcher:
    def __init__(self):
        self._operators: "OrderedDict[int, set]" = OrderedDict()
        self._ticket_to_op: dict = {}

    def add_operator(self, op_id: int) -> None:
        if op_id not in self._operators:
            self._operators[op_id] = set()

    def remove_operator(self, op_id: int) -> list:
        if op_id not in self._operators:
            return []
        tickets = list(self._operators[op_id])
        for t in tickets:
            del self._ticket_to_op[t]
        del self._operators[op_id]
        return tickets

    def assign(self, ticket_id: int) -> "int | None":
        if ticket_id in self._ticket_to_op:
            return self._ticket_to_op[ticket_id]

        if not self._operators:
            return None

        best_op = None
        best_load = None
        for op_id, tickets in self._operators.items():
            load = len(tickets)
            if best_load is None or load < best_load:
                best_load = load
                best_op = op_id

        self._operators[best_op].add(ticket_id)
        self._ticket_to_op[ticket_id] = best_op
        return best_op

    def close(self, ticket_id: int) -> bool:
        op_id = self._ticket_to_op.pop(ticket_id, None)
        if op_id is None:
            return False
        self._operators[op_id].discard(ticket_id)
        return True

    def load(self, op_id: int) -> int:
        if op_id not in self._operators:
            return 0
        return len(self._operators[op_id])


if __name__ == "__main__":
    import asyncio
    from aiogram import Bot, Dispatcher as AiogramDispatcher

    async def main():
        bot = Bot(token="YOUR_TOKEN")
        dp = AiogramDispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())