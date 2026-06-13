from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

MENU = {"Кофе": 150, "Чай": 100, "Десерт": 250}


def build_menu_keyboard() -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text=name)] for name in MENU]
    buttons.append([KeyboardButton(text="Корзина")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def format_price(item: str) -> str:
    if item in MENU:
        return f"{item} — {MENU[item]} руб."
    return "Нет такой позиции"


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать! Выберите позицию:", reply_markup=build_menu_keyboard())


@router.message(F.text.in_(MENU.keys()))
async def handle_menu_choice(message: Message):
    name = message.text
    await message.answer(f"{name} — {MENU[name]} руб. Добавлено в заказ.")


if __name__ == "__main__":
    import asyncio
    from aiogram import Bot, Dispatcher

    async def main():
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())