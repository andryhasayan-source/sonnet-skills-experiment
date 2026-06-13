from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

router = Router()

class Survey(StatesGroup):
    age = State()
    city = State()
    email = State()

QUESTIONS = {"age": "Ваш возраст?", "city": "Ваш город?", "email": "Ваш email?"}
ORDER = ["age", "city", "email"]
_STATES = {"age": Survey.age, "city": Survey.city, "email": Survey.email}

def validate(field, value):
    if field == "age":
        v = value.strip()
        if not v.lstrip("-").isdigit():
            return "Возраст должен быть числом от 1 до 120."
        n = int(v)
        if not (1 <= n <= 120):
            return "Возраст должен быть числом от 1 до 120."
        return None
    if field == "city":
        if len(value.strip()) < 2:
            return "Город слишком короткий."
        return None
    if field == "email":
        v = value.strip()
        if v.count("@") != 1:
            return "Некорректный email."
        local, _, domain = v.partition("@")
        if not local or not domain or "." not in domain:
            return "Некорректный email."
        return None
    return None

async def cmd_survey(message, state):
    await state.set_state(Survey.age)
    await state.update_data(_step="age")
    await message.answer(QUESTIONS["age"])

async def cmd_back(message, state):
    data = await state.get_data()
    step = data.get("_step", "age")
    idx = ORDER.index(step)
    if idx == 0:
        await message.answer("Вы на первом вопросе.")
        return
    prev = ORDER[idx - 1]
    await state.set_state(_STATES[prev])
    await state.update_data(_step=prev)
    await message.answer(QUESTIONS[prev])

async def _process(field, message, state):
    err = validate(field, message.text)
    if err:
        await message.answer(err)
        return
    await state.update_data(**{field: message.text.strip()})
    idx = ORDER.index(field)
    if idx + 1 < len(ORDER):
        nxt = ORDER[idx + 1]
        await state.set_state(_STATES[nxt])
        await state.update_data(_step=nxt)
        await message.answer(QUESTIONS[nxt])
    else:
        data = await state.get_data()
        await message.answer(
            f"Готово! Возраст: {data.get('age')}, город: {data.get('city')}, "
            f"email: {data.get('email')}")
        await state.clear()

async def process_age(message, state):
    await _process("age", message, state)

async def process_city(message, state):
    await _process("city", message, state)

async def process_email(message, state):
    await _process("email", message, state)

if __name__ == "__main__":
    pass
