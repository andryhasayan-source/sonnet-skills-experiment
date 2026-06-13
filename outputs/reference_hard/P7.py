def stable_topk(items, k, key=None):
    if k <= 0:
        return []
    kf = key if key is not None else (lambda x: x)
    decorated = [(kf(x), i, x) for i, x in enumerate(items)]
    # сорт по ключу убыв., при равных — по индексу возр. (стабильность)
    decorated.sort(key=lambda t: t[1])              # вторичный: индекс возр.
    decorated.sort(key=_KeyDesc(lambda t: t[0]))    # первичный: ключ убыв., устойчиво
    return [x for _, _, x in decorated[:k]]

class _KeyDesc:
    """Обёртка для сортировки по убыванию через __lt__, сохраняя стабильность."""
    def __init__(self, getter):
        self.getter = getter
    def __call__(self, item):
        return _Rev(self.getter(item))

class _Rev:
    __slots__ = ("v",)
    def __init__(self, v):
        self.v = v
    def __lt__(self, other):
        return other.v < self.v
    def __eq__(self, other):
        return self.v == other.v
