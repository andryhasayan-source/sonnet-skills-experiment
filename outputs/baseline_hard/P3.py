import re


def evaluate(expr):
    if not isinstance(expr, str):
        return None

    token_re = re.compile(r'\s*(\d+\.\d+|\d+|[()+\-*/])')
    tokens = []
    pos = 0
    while pos < len(expr):
        m = token_re.match(expr, pos)
        if not m:
            if expr[pos:].strip() == '':
                break
            return None
        tok = m.group(1)
        tokens.append(tok)
        pos = m.end()

    if not tokens:
        return None

    state = {'i': 0}

    def peek():
        if state['i'] < len(tokens):
            return tokens[state['i']]
        return None

    def advance():
        t = tokens[state['i']]
        state['i'] += 1
        return t

    def parse_expr():
        val = parse_term()
        if val is None:
            return None
        while peek() in ('+', '-'):
            op = advance()
            rhs = parse_term()
            if rhs is None:
                return None
            val = val + rhs if op == '+' else val - rhs
        return val

    def parse_term():
        val = parse_factor()
        if val is None:
            return None
        while peek() in ('*', '/'):
            op = advance()
            rhs = parse_factor()
            if rhs is None:
                return None
            if op == '*':
                val = val * rhs
            else:
                if rhs == 0:
                    state['div_zero'] = True
                    return None
                val = val / rhs
        return val

    def parse_factor():
        tok = peek()
        if tok == '-':
            advance()
            val = parse_factor()
            if val is None:
                return None
            return -val
        if tok == '+':
            advance()
            return parse_factor()
        return parse_primary()

    def parse_primary():
        tok = peek()
        if tok is None:
            return None
        if tok == '(':
            advance()
            val = parse_expr()
            if val is None:
                return None
            if peek() != ')':
                return None
            advance()
            return val
        if re.match(r'^\d+(\.\d+)?$', tok):
            advance()
            return float(tok)
        return None

    state['div_zero'] = False
    result = parse_expr()
    if result is None:
        return None
    if state['i'] != len(tokens):
        return None
    return float(result)