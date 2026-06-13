import time
from collections import defaultdict, deque

from aiogram import BaseMiddleware, Router


class DualRateLimiter:
    def __init__(self, cmd_limit: int, cmd_window: float, msg_limit: int, msg_window: float):
        self.cmd_limit = cmd_limit
        self.cmd_window = cmd_window
        self.msg_limit = msg_limit
        self.msg_window = msg_window
        self.cmd_history: dict[int, deque] = defaultdict(deque)
        self.msg_history: dict[int, deque] = defaultdict(deque)

    def check(self, user_id: int, is_command: bool, now: float) -> bool:
        if is_command:
            history = self.cmd_history[user_id]
            window = self.cmd_window
            limit = self.cmd_limit
        else:
            history = self.msg_history[user_id]
            window = self.msg_window
            limit = self.msg_limit

        while history and now - history[0] >= window:
            history.popleft()

        if len(history) < limit:
            history.append(now)
            return True
        return False


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, cmd_limit: int = 3, cmd_window: float = 10.0,
                 msg_limit: int = 10, msg_window: float = 10.0):
        super().__init__()
        self.limiter = DualRateLimiter(cmd_limit, cmd_window, msg_limit, msg_window)

    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if user is None:
            return await handler(event, data)

        text = getattr(event, "text", None)
        is_command = text is not None and text.startswith("/")

        now = time.time()
        if self.limiter.check(user.id, is_command, now):
            return await handler(event, data)

        await event.answer("Лимит запросов исчерпан, подождите.")
        return None


router = Router()


if __name__ == "__main__":
    import asyncio
    from aiogram import Bot, Dispatcher

    async def main():
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.message.middleware(RateLimitMiddleware())
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())