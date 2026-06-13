def stable_topk(items: list, k: int, key=None) -> list:
    if k <= 0:
        return []
    if key is None:
        key = lambda x: x
    decorated = sorted(enumerate(items), key=lambda p: (-key(p[1]), p[0]))
    return [item for _, item in decorated[:k]]


if __name__ == "__main__":
    print(stable_topk([3, 1, 2, 3, 1], 2))
    print(stable_topk([("a", 2), ("b", 1), ("c", 2)], 2, key=lambda x: x[1]))