def normalize_phone(raw):
    if not isinstance(raw, str):
        return None
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) == 11 and digits[0] in ("7", "8"):
        return "+7" + digits[1:]
    if len(digits) == 10:
        return "+7" + digits
    return None

def normalize_list(raws):
    valid, invalid, seen = [], [], set()
    for raw in raws:
        norm = normalize_phone(raw)
        if norm is None:
            invalid.append(raw)
        elif norm not in seen:
            seen.add(norm)
            valid.append(norm)
    return {"valid": valid, "invalid": invalid}
