import time
from aiogram import Router, BaseMiddleware

class DualRateLimiter:
    def __init__(self, cmd_limit, cmd_window, msg_limit, msg_window):
        self.cmd_limit, self.cmd_window = cmd_limit, cmd_window
        self.msg_limit, self.msg_window = msg_limit, msg_window
        self._cmd = {}   # user -> [times]
        self._msg = {}

    def _check(self, store, user_id, limit, window, now):
        hits = [t for t in store.get(user_id, []) if t > now - window]
        if len(hits) + 1 <= limit:
            hits.append(now)
            store[user_id] = hits
            return True
        store[user_id] = hits
        return False

    def check(self, user_id, is_command, now):
        if is_command:
            return self._check(self._cmd, user_id, self.cmd_limit,
                               self.cmd_window, now)
        return self._check(self._msg, user_id, self.msg_limit,
                           self.msg_window, now)

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, cmd_limit=3, cmd_window=10.0, msg_limit=10, msg_window=10.0):
        self.limiter = DualRateLimiter(cmd_limit, cmd_window, msg_limit, msg_window)

    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if user is None:
            return await handler(event, data)
        text = getattr(event, "text", None)
        is_command = bool(text) and text.startswith("/")
        if self.limiter.check(user.id, is_command, time.time()):
            return await handler(event, data)
        await event.answer("Лимит запросов исчерпан, подождите.")
        return None

router = Router()

if __name__ == "__main__":
    pass
