import time
import asyncio
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Router, Bot, Dispatcher, F
from aiogram.types import TelegramObject, Message


class ThrottleStorage:
    def __init__(self, limit: int, window: float):
        self.limit = limit
        self.window = window
        self._data: Dict[int, list] = {}

    def hit(self, user_id: int, now: float = None) -> bool:
        if now is None:
            now = time.time()
        timestamps = self._data.setdefault(user_id, [])
        timestamps[:] = [t for t in timestamps if now - t < self.window]
        if len(timestamps) >= self.limit:
            return False
        timestamps.append(now)
        return True


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5, window: float = 10.0):
        super().__init__()
        self.storage = ThrottleStorage(limit, window)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = getattr(event, "from_user", None)
        if user is None:
            return await handler(event, data)

        if self.storage.hit(user.id):
            return await handler(event, data)
        else:
            await event.answer("Слишком часто! Подождите немного.")
            return None


router = Router()


@router.message()
async def echo(message: Message):
    await message.answer(f"ok: {message.text}")


if __name__ == "__main__":
    async def main():
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.message.middleware(AntiFloodMiddleware(limit=5, window=10.0))
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())