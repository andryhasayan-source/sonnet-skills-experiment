import re
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

_DUR_RE = re.compile(r"^(\d+)([smhd])$")
_UNIT_SECONDS = {"s": 1, "m": 60, "h": 3600, "d": 86400}
_FLAG_RE = re.compile(r"^[a-z0-9_]+$")


def parse_duration(token: str) -> int | None:
    m = _DUR_RE.match(token)
    if not m:
        return None
    value, unit = m.groups()
    value = int(value)
    if value <= 0:
        return None
    return value * _UNIT_SECONDS[unit]


def parse_command(text: str) -> dict | None:
    tokens = text.split()
    if not tokens:
        return None

    first = tokens[0]
    if not first.startswith("/") or len(first) < 2:
        return None

    command = first[1:]
    args: list[str] = []
    flags: set[str] = set()

    for token in tokens[1:]:
        if token.startswith("--"):
            name = token[2:]
            if not name or not _FLAG_RE.match(name):
                return None
            flags.add(name)
        else:
            args.append(token)

    return {"command": command, "args": args, "flags": flags}


def build_reminder(text: str) -> dict | None:
    parsed = parse_command(text)
    if parsed is None:
        return None
    if parsed["command"] != "remind":
        return None
    if not parsed["args"]:
        return None

    seconds = parse_duration(parsed["args"][0])
    if seconds is None:
        return None

    message = " ".join(parsed["args"][1:])
    if not message:
        return None

    return {
        "seconds": seconds,
        "message": message,
        "silent": "silent" in parsed["flags"],
    }


@router.message(Command("remind"))
async def handle_remind(message: Message):
    reminder = build_reminder(message.text or "")
    if reminder is None:
        await message.answer(
            "Использование: /remind <время> <текст> [--silent]\n"
            "Пример: /remind 15m купить хлеб --silent"
        )
        return

    await message.answer(
        f"Напоминание установлено через {reminder['seconds']} сек.: "
        f"{reminder['message']}"
        + (" (тихо)" if reminder["silent"] else "")
    )

    async def _reminder_task():
        await asyncio.sleep(reminder["seconds"])
        await message.answer(
            f"⏰ Напоминание: {reminder['message']}",
            disable_notification=reminder["silent"],
        )

    asyncio.create_task(_reminder_task())


if __name__ == "__main__":
    import os

    async def main():
        bot = Bot(token=os.environ["BOT_TOKEN"])
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())