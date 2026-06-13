from aiogram import Router

router = Router()
_ACTIONS = {"view", "edit", "del"}

def _is_clean_int(s, allow_zero):
    if not s.isdigit():
        return False
    if len(s) > 1 and s[0] == "0":  # ведущие нули
        return False
    n = int(s)
    return n >= 0 if allow_zero else n > 0

def pack(action, entity_id, page=0):
    if action not in _ACTIONS or entity_id <= 0 or page < 0:
        raise ValueError("invalid args")
    s = f"act:{action}:{entity_id}:{page}"
    if len(s) > 64:
        raise ValueError("callback_data too long")
    return s

def parse(data):
    if not isinstance(data, str):
        return None
    parts = data.split(":")
    if len(parts) != 4:
        return None
    prefix, action, eid, page = parts
    if prefix != "act" or action not in _ACTIONS:
        return None
    if not _is_clean_int(eid, allow_zero=False):
        return None
    if not _is_clean_int(page, allow_zero=True):
        return None
    return {"action": action, "entity_id": int(eid), "page": int(page)}

async def on_action(callback):
    parsed = parse(callback.data)
    if parsed is None:
        await callback.answer("Некорректная кнопка", show_alert=True)
        return
    await callback.answer()
    await callback.message.answer(
        f"Действие {parsed['action']} над #{parsed['entity_id']} "
        f"(стр. {parsed['page']})")

if __name__ == "__main__":
    pass
