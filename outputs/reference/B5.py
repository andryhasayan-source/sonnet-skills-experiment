import time
from aiogram import Router, BaseMiddleware

class ThrottleStorage:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self._hits = {}

    def hit(self, user_id, now=None):
        now = time.time() if now is None else now
        hits = [t for t in self._hits.get(user_id, []) if t > now - self.window]
        if len(hits) + 1 <= self.limit:
            hits.append(now)
            self._hits[user_id] = hits
            return True
        self._hits[user_id] = hits
        return False

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit=5, window=10.0):
        self.storage = ThrottleStorage(limit, window)

    async def __call__(self, handler, event, data):
        user = getattr(event, "from_user", None)
        if user is None:
            return await handler(event, data)
        if self.storage.hit(user.id):
            return await handler(event, data)
        await event.answer("Слишком часто! Подождите немного.")
        return None

router = Router()

@router.message()
async def echo(message):
    await message.answer(f"ok: {message.text}")

if __name__ == "__main__":
    pass
