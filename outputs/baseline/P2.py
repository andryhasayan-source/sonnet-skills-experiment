"""Модуль для фильтрации лог-файла веб-сервера."""

from typing import Optional


def parse_line(line: str) -> Optional[dict]:
    parts = line.strip().split(" | ")
    if len(parts) != 4:
        return None

    timestamp, level, module, message = parts

    if not timestamp or not level or not module or not message:
        return None

    return {
        "timestamp": timestamp,
        "level": level,
        "module": module,
        "message": message,
    }


def filter_logs(lines: list, level: str = None, module: str = None) -> list:
    result = []
    for line in lines:
        entry = parse_line(line)
        if entry is None:
            continue
        if level is not None and entry["level"] != level:
            continue
        if module is not None and entry["module"] != module:
            continue
        result.append(entry)
    return result


def count_by_level(lines: list) -> dict:
    counts = {}
    for line in lines:
        entry = parse_line(line)
        if entry is None:
            continue
        counts[entry["level"]] = counts.get(entry["level"], 0) + 1
    return counts