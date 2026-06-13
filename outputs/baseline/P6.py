"""Модуль нормализации российских телефонных номеров для CRM."""

import re


def normalize_phone(raw: str) -> str | None:
    if not raw:
        return None

    digits = re.sub(r"\D", "", raw)

    if len(digits) == 10:
        digits = "7" + digits
    elif len(digits) == 11:
        if digits[0] == "8":
            digits = "7" + digits[1:]
        elif digits[0] != "7":
            return None
    else:
        return None

    return "+" + digits


def normalize_list(raws: list[str]) -> dict:
    valid = []
    invalid = []
    seen = set()

    for raw in raws:
        normalized = normalize_phone(raw)
        if normalized is None:
            invalid.append(raw)
        elif normalized not in seen:
            seen.add(normalized)
            valid.append(normalized)

    return {"valid": valid, "invalid": invalid}