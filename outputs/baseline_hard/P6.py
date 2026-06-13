def pretty_duration(seconds: float, max_units: int = 2) -> str:
    if max_units < 1:
        raise ValueError("max_units must be >= 1")
    if seconds < 0:
        raise ValueError("seconds must be non-negative")

    total = int(seconds)  # floor

    if total == 0:
        return "0s"

    d, rem = divmod(total, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)

    values = [d, h, m, s]
    labels = ["d", "h", "m", "s"]

    start = next(i for i, v in enumerate(values) if v != 0)
    end = min(start + max_units, 4)

    return " ".join(f"{values[i]}{labels[i]}" for i in range(start, end))