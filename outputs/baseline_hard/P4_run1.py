import re

_RE = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
    r'(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?'
    r'(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
)
_NUM_ID = re.compile(r'^(0|[1-9]\d*)$')
_VALID_ID = re.compile(r'^[0-9A-Za-z-]+$')


def parse_version(s: str):
    if not isinstance(s, str):
        return None
    m = _RE.match(s)
    if not m:
        return None
    major, minor, patch, pre, build = m.groups()

    pre_ids = ()
    if pre is not None:
        parts = pre.split('.')
        for p in parts:
            if p == '' or not _VALID_ID.match(p):
                return None
            if _NUM_ID.match(p) and len(p) > 1 and p[0] == '0':
                return None
        pre_ids = tuple(parts)

    if build is not None:
        parts = build.split('.')
        for p in parts:
            if p == '' or not _VALID_ID.match(p):
                return None

    return (int(major), int(minor), int(patch), pre_ids)


def _cmp_pre(a, b):
    if a == b:
        return 0
    if not a and b:
        return 1
    if a and not b:
        return -1
    for x, y in zip(a, b):
        if x == y:
            continue
        x_num = _NUM_ID.match(x)
        y_num = _NUM_ID.match(y)
        if x_num and y_num:
            xi, yi = int(x), int(y)
            if xi != yi:
                return -1 if xi < yi else 1
            continue
        if x_num and not y_num:
            return -1
        if not x_num and y_num:
            return 1
        if x != y:
            return -1 if x < y else 1
    if len(a) == len(b):
        return 0
    return -1 if len(a) < len(b) else 1


def compare(a: str, b: str) -> int:
    pa = parse_version(a)
    pb = parse_version(b)
    if pa is None or pb is None:
        raise ValueError("Invalid version string")

    for i in range(3):
        if pa[i] != pb[i]:
            return -1 if pa[i] < pb[i] else 1

    return _cmp_pre(pa[3], pb[3])


if __name__ == '__main__':
    assert compare("1.0.0-alpha", "1.0.0") == -1
    assert compare("1.0.0-alpha", "1.0.0-alpha.1") == -1
    assert compare("1.0.0+a", "1.0.0+b") == 0
    assert parse_version("01.2.3") is None
    assert parse_version("1.2.3-alpha.01") is None
    print("OK")