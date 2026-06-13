import math

_UNITS = [("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]

def pretty_duration(seconds, max_units=2):
    if seconds < 0:
        raise ValueError("seconds must be >= 0")
    if max_units < 1:
        raise ValueError("max_units must be >= 1")
    total = math.floor(seconds)
    if total < 1:
        return "0s"
    # разложим на единицы
    vals = []
    rem = total
    for name, size in _UNITS:
        vals.append((name, rem // size))
        rem = rem % size
    # старшая ненулевая
    start = next(i for i, (_, v) in enumerate(vals) if v > 0)
    chosen = vals[start:start + max_units]
    return " ".join(f"{v}{name}" for name, v in chosen)
