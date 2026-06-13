import time
from collections import deque
from aiogram import BaseMiddleware, Router


class DualRateLimiter:
    def __init__(self, cmd_limit, cmd_window, msg_limit, msg_window):
        self.cmd_limit = cmd_limit
        self.cmd_window = cmd_window
        self.msg_limit = msg_limit
        self.msg_window = msg_window
        self.cmd_hits = {}
        self.msg_hits = {}

    def check(self, user_id: int, is_command: bool, now: float) -> bool:
        if is_command:
            store = self.cmd_hits
            limit = self.cmd_limit
            window = self.cmd_window
        else:
            store = self.msg_hits
            limit = self.msg_limit
            window = self.msg_window

        dq = store.setdefault(user_id, deque())
        while dq and now - dq[0] > window:
            dq.popleft()

        if len(dq) < limit:
            dq.append(now)
            return True
        return False


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, cmd_limit=3, cmd_window=10.0, msg_limit=10, msg_window=10.0):
        self.limiter = DualRateLimiter(cmd_limit, cmd_window, msg_limit, msg_window)

    async def __call__(self, handler, event, data):
        if event.from_user is None:
            return await handler(event, data)

        user_id = event.from_user.id
        text = event.text
        is_command = text is not None and text.startswith("/")
        now = time.time()

        if self.limiter.check(user_id, is_command, now):
            return await handler(event, data)
        else:
            await event.answer("Лимит запросов исчерпан, подождите.")
            return None


router = Router()


if __name__ == "__main__":
    import asyncio
    from aiogram import Bot, Dispatcher
    from aiogram.filters import CommandStart

    @router.message(CommandStart())
    async def start_handler(message):
        await message.answer("Привет!")

    @router.message()
    async def echo_handler(message):
        await message.answer(message.text)

    async def main():
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.message.middleware(RateLimitMiddleware())
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())