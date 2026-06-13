import re

_VER_RE = re.compile(
    r'^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
    r'(?:-(?P<pre>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?'
    r'(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
)


def _is_num_id(s: str) -> bool:
    return s.isdigit()


def _valid_numeric_field(s: str) -> bool:
    if not s.isdigit():
        return False
    if len(s) > 1 and s[0] == '0':
        return False
    return True


def _valid_pre_identifier(s: str) -> bool:
    if s == '':
        return False
    if _is_num_id(s):
        # numeric identifiers must not have leading zeros (unless "0")
        if len(s) > 1 and s[0] == '0':
            return False
    return True


def parse_version(s: str):
    if not isinstance(s, str):
        return None
    m = _VER_RE.match(s)
    if not m:
        return None

    major_s, minor_s, patch_s = m.group('major'), m.group('minor'), m.group('patch')
    if not (_valid_numeric_field(major_s) and _valid_numeric_field(minor_s) and _valid_numeric_field(patch_s)):
        return None

    pre_str = m.group('pre')
    build_str = m.group('build')

    pre_ids = []
    if pre_str is not None:
        parts = pre_str.split('.')
        for p in parts:
            if not _valid_pre_identifier(p):
                return None
            if _is_num_id(p):
                pre_ids.append((0, int(p)))
            else:
                pre_ids.append((1, p))

    build_ids = []
    if build_str is not None:
        parts = build_str.split('.')
        for p in parts:
            if p == '':
                return None
            build_ids.append(p)

    return (
        int(major_s),
        int(minor_s),
        int(patch_s),
        tuple(pre_ids),
        tuple(build_ids),
    )


def _compare_pre(a_pre, b_pre):
    # No pre-release > has pre-release
    if not a_pre and not b_pre:
        return 0
    if not a_pre and b_pre:
        return 1
    if a_pre and not b_pre:
        return -1

    for ai, bi in zip(a_pre, b_pre):
        a_type, a_val = ai
        b_type, b_val = bi
        if a_type != b_type:
            # numeric (0) < non-numeric (1)
            return -1 if a_type < b_type else 1
        if a_val != b_val:
            return -1 if a_val < b_val else 1

    if len(a_pre) != len(b_pre):
        return -1 if len(a_pre) < len(b_pre) else 1
    return 0


def compare(a: str, b: str) -> int:
    pa = parse_version(a)
    pb = parse_version(b)
    if pa is None or pb is None:
        raise ValueError("Invalid version string")

    a_major, a_minor, a_patch, a_pre, _ = pa
    b_major, b_minor, b_patch, b_pre, _ = pb

    for x, y in ((a_major, b_major), (a_minor, b_minor), (a_patch, b_patch)):
        if x != y:
            return -1 if x < y else 1

    return _compare_pre(a_pre, b_pre)


if __name__ == '__main__':
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

    for bad in ["1.01.0", "1.2.3-01", "1.2", "1.2.3.4", "-1.0.0", "1.2.3-", "1.2.3+"]:
        assert parse_version(bad) is None, f"{bad} should be invalid"

    print("All tests passed.")