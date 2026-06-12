from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

router = Router()

class OrderForm(StatesGroup):
    name = State()
    phone = State()

def is_valid_phone(raw):
    if not isinstance(raw, str):
        return False
    digits = sum(ch.isdigit() for ch in raw)
    return 10 <= digits <= 11

@router.message(Command("order"))
async def cmd_order(message, state):
    await state.set_state(OrderForm.name)
    await message.answer("Как вас зовут?")

@router.message(OrderForm.name)
async def process_name(message, state):
    if len(message.text.strip()) < 2:
        await message.answer("Имя слишком короткое, попробуйте ещё раз.")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(OrderForm.phone)
    await message.answer("Укажите телефон:")

@router.message(OrderForm.phone)
async def process_phone(message, state):
    if not is_valid_phone(message.text):
        await message.answer("Телефон некорректен, попробуйте ещё раз.")
        return
    data = await state.get_data()
    name = data.get("name", "")
    await message.answer(f"Спасибо, {name}! Заказ принят, мы перезвоним.")
    await state.clear()

if __name__ == "__main__":
    pass
