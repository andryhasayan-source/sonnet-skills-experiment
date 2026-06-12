def parse_line(line):
    if not isinstance(line, str):
        return None
    parts = line.split(" | ")
    if len(parts) != 4:
        return None
    ts, level, module, message = parts
    if not ts.strip() or not level.strip():
        return None
    return {"timestamp": ts.strip(), "level": level.strip(),
            "module": module.strip(), "message": message.strip()}

def filter_logs(lines, level=None, module=None):
    out = []
    for line in lines:
        rec = parse_line(line)
        if rec is None:
            continue
        if level is not None and rec["level"] != level:
            continue
        if module is not None and rec["module"] != module:
            continue
        out.append(rec)
    return out

def count_by_level(lines):
    counts = {}
    for line in lines:
        rec = parse_line(line)
        if rec is None:
            continue
        counts[rec["level"]] = counts.get(rec["level"], 0) + 1
    return counts
