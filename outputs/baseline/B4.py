from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

ITEMS = [f"Товар {i}" for i in range(1, 24)]
PAGE_SIZE = 5


def get_page(items: list, page: int, page_size: int = PAGE_SIZE) -> list:
    start = page * page_size
    if start < 0 or start >= len(items):
        return []
    return items[start:start + page_size]


def total_pages(items: list, page_size: int = PAGE_SIZE) -> int:
    if not items:
        return 0
    return (len(items) + page_size - 1) // page_size


def build_page_text(items: list, page: int) -> str:
    pages = total_pages(items, PAGE_SIZE)
    lines = [f"Страница {page + 1}/{pages}:"]
    for item in get_page(items, page):
        lines.append(f"- {item}")
    return "\n".join(lines)


def build_pager_keyboard(page: int, pages: int) -> InlineKeyboardMarkup:
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="<<", callback_data=f"page:{page-1}"))
    if page < pages - 1:
        buttons.append(InlineKeyboardButton(text=">>", callback_data=f"page:{page+1}"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons] if buttons else [[]])


@router.message(Command("catalog"))
async def cmd_catalog(message: Message):
    page = 0
    pages = total_pages(ITEMS, PAGE_SIZE)
    await message.answer(build_page_text(ITEMS, page), reply_markup=build_pager_keyboard(page, pages))


@router.callback_query(F.data.startswith("page:"))
async def on_page(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    pages = total_pages(ITEMS, PAGE_SIZE)
    await callback.message.edit_text(build_page_text(ITEMS, page), reply_markup=build_pager_keyboard(page, pages))
    await callback.answer()


if __name__ == "__main__":
    import asyncio

    async def main():
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())