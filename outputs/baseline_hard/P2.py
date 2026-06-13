import copy

DELETE = object()


def deep_merge(base: dict, override: dict) -> dict:
    result = {}
    for key, value in base.items():
        result[key] = copy.deepcopy(value)

    for key, value in override.items():
        if value is DELETE:
            result.pop(key, None)
            continue

        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)

    return result


if __name__ == "__main__":
    base = {
        "db": {"host": "localhost", "port": 5432, "options": {"ssl": False}},
        "tags": ["a", "b"],
        "debug": False,
        "obsolete": "to_remove",
    }
    override = {
        "db": {"port": 6543, "options": {"ssl": True}},
        "tags": ["x"],
        "obsolete": DELETE,
        "new_key": 42,
    }

    merged = deep_merge(base, override)
    print(merged)
    print(base)
    print(override)