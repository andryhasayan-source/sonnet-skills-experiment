import re
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import CallbackQuery

ACTIONS = {"view", "edit", "del"}
_NUM_RE = re.compile(r"^(0|[1-9]\d*)$")


def pack(action: str, entity_id: int, page: int = 0) -> str:
    if action not in ACTIONS:
        raise ValueError("invalid action")
    if entity_id <= 0:
        raise ValueError("entity_id must be positive")
    if page < 0:
        raise ValueError("page must be non-negative")
    result = f"act:{action}:{entity_id}:{page}"
    if len(result) > 64:
        raise ValueError("callback_data too long")
    return result


def parse(data: str) -> dict | None:
    parts = data.split(":")
    if len(parts) != 4:
        return None
    prefix, action, entity_id_s, page_s = parts
    if prefix != "act":
        return None
    if action not in ACTIONS:
        return None
    if not _NUM_RE.match(entity_id_s) or not _NUM_RE.match(page_s):
        return None
    entity_id = int(entity_id_s)
    page = int(page_s)
    if entity_id <= 0:
        return None
    if page < 0:
        return None
    return {"action": action, "entity_id": entity_id, "page": page}


router = Router()


@router.callback_query(F.data.startswith("act:"))
async def on_action(callback: CallbackQuery):
    parsed = parse(callback.data)
    if parsed is None:
        await callback.answer("Некорректная кнопка", show_alert=True)
        return
    await callback.answer()
    await callback.message.answer(
        f"Действие {parsed['action']} над #{parsed['entity_id']} (стр. {parsed['page']})"
    )


if __name__ == "__main__":
    import asyncio

    BOT_TOKEN = "YOUR_BOT_TOKEN"

    async def main():
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())