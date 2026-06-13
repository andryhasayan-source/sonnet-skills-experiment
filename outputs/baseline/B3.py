import re
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


class OrderForm(StatesGroup):
    name = State()
    phone = State()


@router.message(Command("order"))
async def cmd_order(message: Message, state: FSMContext):
    await state.set_state(OrderForm.name)
    await message.answer("Как вас зовут?")


@router.message(OrderForm.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("Имя слишком короткое, попробуйте ещё раз.")
        return
    await state.update_data(name=name)
    await state.set_state(OrderForm.phone)
    await message.answer("Укажите телефон:")


def is_valid_phone(raw: str) -> bool:
    digits = re.sub(r"\D", "", raw)
    return 10 <= len(digits) <= 11


@router.message(OrderForm.phone)
async def process_phone(message: Message, state: FSMContext):
    if not is_valid_phone(message.text):
        await message.answer("Телефон некорректен, попробуйте ещё раз.")
        return
    data = await state.get_data()
    name = data.get("name")
    await message.answer(f"Спасибо, {name}! Заказ принят, мы перезвоним.")
    await state.clear()


if __name__ == "__main__":
    import asyncio
    from aiogram import Bot, Dispatcher

    async def main():
        bot = Bot(token="YOUR_BOT_TOKEN")
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(main())