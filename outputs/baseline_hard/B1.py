"""
Модуль корзины интернет-магазина для Telegram-бота на aiogram 3.x.

Логика корзины полностью инкапсулирована в классе Cart (тестируется
без какого-либо обращения к Telegram API). Обработчики — тонкие
обёртки, которые парсят команды и вызывают методы Cart / cart_summary.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


# ---------------------------------------------------------------------------
# Бизнес-логика
# ---------------------------------------------------------------------------

class Cart:
    """Корзина интернет-магазина.

    Хранит для каждого пользователя словарь {товар: количество}.
    Порядок ключей в словаре соответствует порядку, в котором товар
    впервые появился в корзине (или появился повторно после удаления).
    """

    def __init__(self):
        # user_id -> {product: qty}
        self._carts: dict[int, dict[str, int]] = {}

    def add(self, user_id, product, qty=1) -> int:
        """Добавляет qty штук товара. Возвращает новое суммарное количество."""
        if qty <= 0:
            raise ValueError("qty must be positive")

        cart = self._carts.setdefault(user_id, {})
        new_qty = cart.get(product, 0) + qty
        cart[product] = new_qty
        return new_qty

    def remove(self, user_id, product, qty=1) -> int:
        """Убирает qty штук товара.

        Если количество становится <= 0, товар полностью удаляется
        из корзины и возвращается 0. Если товара в корзине не было —
        также возвращается 0 (без ошибки).
        """
        if qty <= 0:
            raise ValueError("qty must be positive")

        cart = self._carts.get(user_id)
        if not cart or product not in cart:
            return 0

        new_qty = cart[product] - qty
        if new_qty <= 0:
            del cart[product]
            return 0

        cart[product] = new_qty
        return new_qty

    def items(self, user_id) -> dict:
        """Возвращает копию словаря товаров пользователя."""
        return dict(self._carts.get(user_id, {}))

    def total_qty(self, user_id) -> int:
        """Суммарное количество всех товаров в корзине пользователя."""
        return sum(self._carts.get(user_id, {}).values())

    def clear(self, user_id) -> None:
        """Полностью очищает корзину пользователя."""
        self._carts.pop(user_id, None)


# ---------------------------------------------------------------------------
# Каталог цен и форматирование сводки
# ---------------------------------------------------------------------------

PRICES = {"apple": 50, "bread": 40, "milk": 80}


def cart_summary(cart: Cart, user_id: int) -> str:
    """Текстовая сводка корзины пользователя."""
    items = cart.items(user_id)
    if not items:
        return "Корзина пуста."

    lines = []
    total = 0
    for product, qty in items.items():
        price = PRICES.get(product, 0)
        line_total = price * qty
        total += line_total
        lines.append(f"{product} x{qty} = {line_total} руб.")

    lines.append(f"Итого: {total} руб.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Telegram-обработчики (тонкие обёртки)
# ---------------------------------------------------------------------------

router = Router()

# Глобальный экземпляр корзины, используемый обработчиками.
cart = Cart()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я бот-магазин.\n"
        "Команды:\n"
        "/add <товар> [кол-во] — добавить товар в корзину\n"
        "/remove <товар> [кол-во] — убрать товар из корзины\n"
        "/cart — показать корзину\n"
        "/clear — очистить корзину\n\n"
        f"Доступные товары: {', '.join(PRICES.keys())}"
    )


@router.message(Command("add"))
async def cmd_add(message: Message) -> None:
    args = (message.text or "").split()[1:]
    if not args:
        await message.answer("Использование: /add <товар> [количество]")
        return

    product = args[0]
    qty = 1
    if len(args) > 1:
        try:
            qty = int(args[1])
        except ValueError:
            await message.answer("Количество должно быть целым числом.")
            return

    try:
        new_qty = cart.add(message.from_user.id, product, qty)
    except ValueError:
        await message.answer("Количество должно быть положительным числом.")
        return

    await message.answer(f"«{product}»: теперь в корзине {new_qty} шт.")


@router.message(Command("remove"))
async def cmd_remove(message: Message) -> None:
    args = (message.text or "").split()[1:]
    if not args:
        await message.answer("Использование: /remove <товар> [количество]")
        return

    product = args[0]
    qty = 1
    if len(args) > 1:
        try:
            qty = int(args[1])
        except ValueError:
            await message.answer("Количество должно быть целым числом.")
            return

    try:
        new_qty = cart.remove(message.from_user.id, product, qty)
    except ValueError:
        await message.answer("Количество должно быть положительным числом.")
        return

    if new_qty == 0:
        await message.answer(f"«{product}» удалён из корзины.")
    else:
        await message.answer(f"«{product}»: осталось {new_qty} шт.")


@router.message(Command("cart"))
async def cmd_cart(message: Message) -> None:
    await message.answer(cart_summary(cart, message.from_user.id))


@router.message(Command("clear"))
async def cmd_clear(message: Message) -> None:
    cart.clear(message.from_user.id)
    await message.answer("Корзина очищена.")


# ---------------------------------------------------------------------------
# Запуск бота
# ---------------------------------------------------------------------------

async def main() -> None:
    bot = Bot(token="YOUR_BOT_TOKEN")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())