_VALUES = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),
           (90,"XC"),(50,"L"),(40,"XL"),(10,"X"),(9,"IX"),
           (5,"V"),(4,"IV"),(1,"I")]

def int_to_roman(n):
    if not isinstance(n, int) or isinstance(n, bool) or not (1 <= n <= 3999):
        raise ValueError("n must be int in 1..3999")
    out = []
    for val, sym in _VALUES:
        while n >= val:
            out.append(sym)
            n -= val
    return "".join(out)

def roman_to_int(s):
    if not isinstance(s, str):
        raise ValueError("expected str")
    vals = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    if not s or any(ch not in vals for ch in s):
        raise ValueError("invalid roman")
    total, i, prev = 0, 0, None
    for ch in s:
        v = vals[ch]
        total += v
        if prev is not None and prev < v:
            total -= 2 * prev
        prev = v
    # каноничность: единственный надёжный критерий
    if int_to_roman(total) != s:
        raise ValueError("non-canonical roman")
    return total
