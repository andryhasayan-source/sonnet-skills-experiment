from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

MENU = {"Кофе": 150, "Чай": 100, "Десерт": 250}

def build_menu_keyboard():
    rows = [[KeyboardButton(text=name)] for name in MENU]
    rows.append([KeyboardButton(text="Корзина")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

def format_price(item):
    if item not in MENU:
        return "Нет такой позиции"
    return f"{item} — {MENU[item]} руб."

@router.message(Command("start"))
async def cmd_start(message):
    await message.answer("Добро пожаловать! Выберите позицию:",
                         reply_markup=build_menu_keyboard())

@router.message(F.text.in_(MENU.keys()))
async def handle_menu_choice(message):
    await message.answer(f"{message.text} — {MENU[message.text]} руб. Добавлено в заказ.")

if __name__ == "__main__":
    pass
