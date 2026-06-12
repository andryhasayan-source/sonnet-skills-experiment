def merge_intervals(intervals):
    if not intervals:
        return []
    items = sorted(intervals)
    merged = [list(items[0])]
    for s, e in items[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [tuple(x) for x in merged]

def free_slots(busy, day_start, day_end):
    merged = merge_intervals(busy)
    clipped = []
    for s, e in merged:
        s, e = max(s, day_start), min(e, day_end)
        if s < e:
            clipped.append((s, e))
    free, cur = [], day_start
    for s, e in clipped:
        if s > cur:
            free.append((cur, s))
        cur = max(cur, e)
    if cur < day_end:
        free.append((cur, day_end))
    return free

def find_slot(busy, duration, day_start, day_end):
    for s, e in free_slots(busy, day_start, day_end):
        if e - s >= duration:
            return (s, s + duration)
    return None
