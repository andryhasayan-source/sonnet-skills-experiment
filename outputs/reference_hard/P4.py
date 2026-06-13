import re

_NUM = re.compile(r"^(0|[1-9][0-9]*)$")
_CORE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

def _valid_num(part):
    return bool(_NUM.match(part))

def parse_version(s):
    if not isinstance(s, str) or not s:
        return None
    build = None
    if "+" in s:
        s, build = s.split("+", 1)
        if not build or any(not _id_ok_build(x) for x in build.split(".")):
            return None
    pre = None
    if "-" in s:
        s, pre = s.split("-", 1)
    m = _CORE.match(s)
    if not m:
        return None
    nums = []
    for g in m.groups():
        if not _valid_num(g):
            return None
        nums.append(int(g))
    pre_ids = None
    if pre is not None:
        if pre == "" or pre.startswith(".") or pre.endswith(".") or ".." in pre:
            return None
        pre_ids = []
        for ident in pre.split("."):
            if ident == "":
                return None
            if ident.isdigit():
                if len(ident) > 1 and ident[0] == "0":
                    return None
                pre_ids.append((0, int(ident)))
            else:
                if not re.match(r"^[0-9A-Za-z-]+$", ident):
                    return None
                pre_ids.append((1, ident))
    return (nums[0], nums[1], nums[2], pre_ids)

def _id_ok_build(x):
    return bool(re.match(r"^[0-9A-Za-z-]+$", x))

def compare(a, b):
    pa, pb = parse_version(a), parse_version(b)
    if pa is None or pb is None:
        raise ValueError("invalid version")
    for i in range(3):
        if pa[i] != pb[i]:
            return -1 if pa[i] < pb[i] else 1
    apre, bpre = pa[3], pb[3]
    if apre is None and bpre is None:
        return 0
    if apre is None:
        return 1   # без пререлиза больше
    if bpre is None:
        return -1
    for x, y in zip(apre, bpre):
        if x == y:
            continue
        # числовой (0,..) < нечисловой (1,..)
        if x[0] != y[0]:
            return -1 if x[0] < y[0] else 1
        if x[1] != y[1]:
            return -1 if x[1] < y[1] else 1
    if len(apre) != len(bpre):
        return -1 if len(apre) < len(bpre) else 1
    return 0
