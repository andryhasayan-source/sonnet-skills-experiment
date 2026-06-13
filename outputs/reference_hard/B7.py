import re
from aiogram import Router

router = Router()

_UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400}
_FLAG_RE = re.compile(r"^[a-z0-9_]+$")

def parse_duration(token):
    if not isinstance(token, str) or len(token) < 2:
        return None
    suffix = token[-1]
    if suffix not in _UNITS:
        return None
    num = token[:-1]
    if not num.isdigit():
        return None
    n = int(num)
    if n <= 0:
        return None
    return n * _UNITS[suffix]

def parse_command(text):
    if not isinstance(text, str) or not text.strip():
        return None
    tokens = text.split()
    first = tokens[0]
    if not first.startswith("/") or len(first) < 2:
        return None
    command = first[1:]
    args, flags = [], set()
    for tok in tokens[1:]:
        if tok.startswith("--"):
            name = tok[2:]
            if not name or not _FLAG_RE.match(name):
                return None
            flags.add(name)
        else:
            args.append(tok)
    return {"command": command, "args": args, "flags": flags}

def build_reminder(text):
    parsed = parse_command(text)
    if parsed is None or parsed["command"] != "remind":
        return None
    args = parsed["args"]
    if not args:
        return None
    seconds = parse_duration(args[0])
    if seconds is None:
        return None
    message = " ".join(args[1:]).strip()
    if not message:
        return None
    return {"seconds": seconds, "message": message,
            "silent": "silent" in parsed["flags"]}

if __name__ == "__main__":
    pass
