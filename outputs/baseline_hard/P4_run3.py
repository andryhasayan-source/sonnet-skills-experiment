import re

_RE = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
    r'(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?'
    r'(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
)

_ID_RE = re.compile(r'^[0-9A-Za-z-]+$')
_NUM_RE = re.compile(r'^(0|[1-9]\d*)$')


def parse_version(s: str):
    if not isinstance(s, str):
        return None
    m = _RE.match(s)
    if not m:
        return None

    major, minor, patch, pre, build = m.groups()
    major, minor, patch = int(major), int(minor), int(patch)

    pre_ids = []
    if pre is not None:
        for part in pre.split('.'):
            if part == '' or not _ID_RE.match(part):
                return None
            pre_ids.append(part)

    build_ids = []
    if build is not None:
        for part in build.split('.'):
            if part == '' or not _ID_RE.match(part):
                return None
            build_ids.append(part)

    return (major, minor, patch, tuple(pre_ids), tuple(build_ids))


def _cmp_pre_ids(a_ids, b_ids):
    if not a_ids and not b_ids:
        return 0
    if not a_ids:
        return 1   # no prerelease > has prerelease
    if not b_ids:
        return -1

    for a, b in zip(a_ids, b_ids):
        a_num = _NUM_RE.match(a)
        b_num = _NUM_RE.match(b)

        if a_num and b_num:
            ai, bi = int(a), int(b)
            if ai != bi:
                return -1 if ai < bi else 1
        elif a_num and not b_num:
            return -1
        elif not a_num and b_num:
            return 1
        else:
            if a != b:
                return -1 if a < b else 1

    if len(a_ids) != len(b_ids):
        return -1 if len(a_ids) < len(b_ids) else 1
    return 0


def compare(a: str, b: str) -> int:
    pa = parse_version(a)
    pb = parse_version(b)
    if pa is None or pb is None:
        raise ValueError("Invalid version string")

    for i in range(3):
        if pa[i] != pb[i]:
            return -1 if pa[i] < pb[i] else 1

    return _cmp_pre_ids(pa[3], pb[3])


if __name__ == "__main__":
    tests = [
        ("1.0.0-alpha", "1.0.0", -1),
        ("1.0.0-alpha", "1.0.0-alpha.1", -1),
        ("1.0.0-alpha.1", "1.0.0-alpha.beta", -1),
        ("1.0.0-alpha.beta", "1.0.0-beta", -1),
        ("1.0.0-beta", "1.0.0-beta.2", -1),
        ("1.0.0-beta.2", "1.0.0-beta.11", -1),
        ("1.0.0-beta.11", "1.0.0-rc.1", -1),
        ("1.0.0-rc.1", "1.0.0", -1),
        ("1.0.0+a", "1.0.0+b", 0),
        ("1.2.3", "1.2.3", 0),
        ("2.0.0", "1.9.9", 1),
    ]
    for a, b, exp in tests:
        res = compare(a, b)
        assert res == exp, f"{a} vs {b}: got {res}, expected {exp}"

    assert parse_version("01.0.0") is None
    assert parse_version("1.0.0-") is None
    assert parse_version("1.0.0-alpha.") is None
    assert parse_version("1.0.0-alpha..1") is None
    assert parse_version("1.2") is None
    assert parse_version("-1.0.0") is None

    print("All tests passed.")