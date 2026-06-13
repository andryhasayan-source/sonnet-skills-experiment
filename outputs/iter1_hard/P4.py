import re

VERSION_RE = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
    r'(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?'
    r'(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
)

IDENT_RE = re.compile(r'^[0-9A-Za-z-]+$')
NUMERIC_RE = re.compile(r'^(0|[1-9]\d*)$')


def parse_version(s: str):
    if not isinstance(s, str):
        return None
    m = VERSION_RE.match(s)
    if not m:
        return None
    major, minor, patch, pre, build = m.groups()
    pre_idents = tuple(pre.split('.')) if pre else ()
    for ident in pre_idents:
        if not IDENT_RE.match(ident) or ident == '':
            return None
        if NUMERIC_RE.match(ident) is None and ident.isdigit():
            # leading zero numeric identifier like "01"
            return None
    if build:
        for ident in build.split('.'):
            if not IDENT_RE.match(ident) or ident == '':
                return None
    return (int(major), int(minor), int(patch), pre_idents)


def _compare_pre(a_pre, b_pre):
    if a_pre == b_pre:
        return 0
    if not a_pre and b_pre:
        return 1
    if a_pre and not b_pre:
        return -1

    for a_id, b_id in zip(a_pre, b_pre):
        a_num = NUMERIC_RE.match(a_id) is not None
        b_num = NUMERIC_RE.match(b_id) is not None
        if a_num and b_num:
            ai, bi = int(a_id), int(b_id)
            if ai != bi:
                return -1 if ai < bi else 1
        elif a_num and not b_num:
            return -1
        elif not a_num and b_num:
            return 1
        else:
            if a_id != b_id:
                return -1 if a_id < b_id else 1

    if len(a_pre) != len(b_pre):
        return -1 if len(a_pre) < len(b_pre) else 1
    return 0


def compare(a: str, b: str) -> int:
    pa = parse_version(a)
    pb = parse_version(b)
    if pa is None or pb is None:
        raise ValueError("Invalid version string")

    for x, y in zip(pa[:3], pb[:3]):
        if x != y:
            return -1 if x < y else 1

    return _compare_pre(pa[3], pb[3])