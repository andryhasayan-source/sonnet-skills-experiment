def evaluate(expr):
    if not isinstance(expr, str):
        return None
    s = expr
    pos = 0
    n = len(s)

    def skip_ws():
        nonlocal pos
        while pos < n and s[pos] == " ":
            pos += 1

    def parse_expr():
        val = parse_term()
        if val is None:
            return None
        while True:
            skip_ws()
            if pos < n and s[pos] in "+-":
                op = s[pos]
                bump()
                rhs = parse_term()
                if rhs is None:
                    return None
                val = val + rhs if op == "+" else val - rhs
            else:
                break
        return val

    def parse_term():
        val = parse_factor()
        if val is None:
            return None
        while True:
            skip_ws()
            if pos < n and s[pos] in "*/":
                op = s[pos]
                bump()
                rhs = parse_factor()
                if rhs is None:
                    return None
                if op == "*":
                    val = val * rhs
                else:
                    if rhs == 0:
                        raise ZeroDivisionError
                    val = val / rhs
            else:
                break
        return val

    def bump():
        nonlocal pos
        pos += 1

    def parse_factor():
        skip_ws()
        if pos >= n:
            return None
        if s[pos] == "+":
            bump()
            return parse_factor()
        if s[pos] == "-":
            bump()
            v = parse_factor()
            return None if v is None else -v
        if s[pos] == "(":
            bump()
            v = parse_expr()
            if v is None:
                return None
            skip_ws()
            if pos >= n or s[pos] != ")":
                return None
            bump()
            return v
        return parse_number()

    def parse_number():
        nonlocal pos
        start = pos
        seen_dot = False
        while pos < n and (s[pos].isdigit() or s[pos] == "."):
            if s[pos] == ".":
                if seen_dot:
                    return None
                seen_dot = True
            pos += 1
        if pos == start:
            return None
        tok = s[start:pos]
        if tok == ".":
            return None
        try:
            return float(tok)
        except ValueError:
            return None

    try:
        result = parse_expr()
    except ZeroDivisionError:
        return None
    if result is None:
        return None
    skip_ws()
    if pos != n:
        return None
    return float(result)
