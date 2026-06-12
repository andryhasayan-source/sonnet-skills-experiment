import math
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

ITEMS = [f"Товар {i}" for i in range(1, 24)]
PAGE_SIZE = 5

def get_page(items, page, page_size=PAGE_SIZE):
    if page < 0:
        return []
    start = page * page_size
    return items[start:start + page_size]

def total_pages(items, page_size=PAGE_SIZE):
    return math.ceil(len(items) / page_size) if items else 0

def build_page_text(items, page):
    pages = total_pages(items)
    lines = [f"Страница {page + 1}/{pages}:"]
    for item in get_page(items, page):
        lines.append(f"- {item}")
    return "\n".join(lines)

def build_pager_keyboard(page, pages):
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="<<", callback_data=f"page:{page - 1}"))
    if page < pages - 1:
        buttons.append(InlineKeyboardButton(text=">>", callback_data=f"page:{page + 1}"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons] if buttons else [[]])

@router.message(Command("catalog"))
async def cmd_catalog(message):
    pages = total_pages(ITEMS)
    await message.answer(build_page_text(ITEMS, 0),
                         reply_markup=build_pager_keyboard(0, pages))

@router.callback_query(F.data.startswith("page:"))
async def on_page(callback):
    page = int(callback.data.split(":")[1])
    pages = total_pages(ITEMS)
    await callback.message.edit_text(build_page_text(ITEMS, page),
                                     reply_markup=build_pager_keyboard(page, pages))
    await callback.answer()

if __name__ == "__main__":
    pass
