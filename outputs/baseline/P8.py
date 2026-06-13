import time
from collections import OrderedDict


class TTLCache:
    def __init__(self, max_size: int, ttl_seconds: float):
        if max_size < 1:
            raise ValueError("max_size must be >= 1")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be > 0")
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._data: OrderedDict = OrderedDict()

    def set(self, key, value, now: float = None) -> None:
        if now is None:
            now = time.time()
        if key in self._data:
            del self._data[key]
        self._data[key] = (value, now + self.ttl_seconds)
        self._data.move_to_end(key)
        if len(self._data) > self.max_size:
            self._data.popitem(last=False)

    def get(self, key, now: float = None):
        if now is None:
            now = time.time()
        if key not in self._data:
            return None
        value, expires_at = self._data[key]
        if expires_at <= now:
            del self._data[key]
            return None
        self._data.move_to_end(key)
        return value

    def __len__(self) -> int:
        now = time.time()
        return sum(1 for _, exp in self._data.values() if exp > now)