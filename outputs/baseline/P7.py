def merge_intervals(intervals: list[tuple]) -> list[tuple]:
    if not intervals:
        return []
    sorted_intervals = sorted(intervals)
    merged = [sorted_intervals[0]]
    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def free_slots(busy: list[tuple], day_start: int, day_end: int) -> list[tuple]:
    clipped = []
    for start, end in busy:
        s = max(start, day_start)
        e = min(end, day_end)
        if s < e:
            clipped.append((s, e))

    merged = merge_intervals(clipped)

    free = []
    cursor = day_start
    for start, end in merged:
        if cursor < start:
            free.append((cursor, start))
        cursor = max(cursor, end)
    if cursor < day_end:
        free.append((cursor, day_end))

    return free


def find_slot(busy: list[tuple], duration: int, day_start: int, day_end: int) -> tuple | None:
    for start, end in free_slots(busy, day_start, day_end):
        if end - start >= duration:
            return (start, start + duration)
    return None