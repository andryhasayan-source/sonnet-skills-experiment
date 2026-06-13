class _CalcError(Exception):
    pass


def _tokenize(s: str):
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c in '+-*/()':
            tokens.append(c)
            i += 1
            continue
        if c.isdigit() or c == '.':
            j = i
            dot_count = 0
            while j < n and (s[j].isdigit() or s[j] == '.'):
                if s[j] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        raise _CalcError("invalid number")
                j += 1
            num_str = s[i:j]
            if num_str == '.' or num_str.startswith('.') and len(num_str) == 1:
                raise _CalcError("invalid number")
            if num_str.startswith('.'):
                num_str = '0' + num_str
            if num_str.endswith('.'):
                num_str = num_str + '0'
            tokens.append(('NUM', float(num_str)))
            i = j
            continue
        raise _CalcError(f"unexpected character: {c}")
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def parse_expr(self):
        value = self.parse_term()
        while True:
            tok = self.peek()
            if tok == '+' or tok == '-':
                self.advance()
                rhs = self.parse_term()
                if tok == '+':
                    value = value + rhs
                else:
                    value = value - rhs
            else:
                break
        return value

    def parse_term(self):
        value = self.parse_factor()
        while True:
            tok = self.peek()
            if tok == '*' or tok == '/':
                self.advance()
                rhs = self.parse_factor()
                if tok == '*':
                    value = value * rhs
                else:
                    if rhs == 0:
                        raise _CalcError("division by zero")
                    value = value / rhs
            else:
                break
        return value

    def parse_factor(self):
        tok = self.peek()
        if tok == '-':
            self.advance()
            return -self.parse_factor()
        if tok == '+':
            self.advance()
            return self.parse_factor()
        return self.parse_primary()

    def parse_primary(self):
        tok = self.peek()
        if tok is None:
            raise _CalcError("unexpected end of expression")
        if isinstance(tok, tuple) and tok[0] == 'NUM':
            self.advance()
            return tok[1]
        if tok == '(':
            self.advance()
            value = self.parse_expr()
            if self.peek() != ')':
                raise _CalcError("expected closing parenthesis")
            self.advance()
            return value
        raise _CalcError(f"unexpected token: {tok}")


def evaluate(expr: str) -> float | None:
    if not isinstance(expr, str):
        return None
    if expr.strip() == '':
        return None
    try:
        tokens = _tokenize(expr)
        if not tokens:
            return None
        parser = _Parser(tokens)
        result = parser.parse_expr()
        if parser.pos != len(parser.tokens):
            return None
        return float(result)
    except _CalcError:
        return None
    except ZeroDivisionError:
        return None