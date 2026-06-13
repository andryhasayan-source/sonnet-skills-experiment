"""Strict Roman numeral conversion module."""

import re

_VALUES = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
    (1, "I"),
]

_ROMAN_RE = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)


def int_to_roman(n: int) -> str:
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n must be an int")
    if not (1 <= n <= 3999):
        raise ValueError("n must be in range 1..3999")

    result = []
    for value, symbol in _VALUES:
        count, n = divmod(n, value)
        result.append(symbol * count)
    return "".join(result)


def roman_to_int(s: str) -> int:
    if not isinstance(s, str):
        raise ValueError("s must be a str")
    if not s or not _ROMAN_RE.fullmatch(s):
        raise ValueError(f"Invalid roman numeral: {s!r}")

    total = 0
    i = 0
    for value, symbol in _VALUES:
        while s[i:i + len(symbol)] == symbol:
            total += value
            i += len(symbol)
    return total