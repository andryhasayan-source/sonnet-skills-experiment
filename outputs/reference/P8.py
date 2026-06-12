import time
from collections import OrderedDict

class TTLCache:
    def __init__(self, max_size, ttl_seconds):
        if max_size < 1:
            raise ValueError("max_size must be >= 1")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be > 0")
        self.max_size = max_size
        self.ttl = ttl_seconds
        self._data = OrderedDict()  # key -> (value, expires_at)

    def _purge(self, now):
        dead = [k for k, (_, exp) in self._data.items() if exp <= now]
        for k in dead:
            del self._data[k]

    def set(self, key, value, now=None):
        now = time.time() if now is None else now
        self._purge(now)
        if key in self._data:
            del self._data[key]
        self._data[key] = (value, now + self.ttl)
        while len(self._data) > self.max_size:
            self._data.popitem(last=False)  # вытесняем LRU

    def get(self, key, now=None):
        now = time.time() if now is None else now
        item = self._data.get(key)
        if item is None:
            return None
        value, exp = item
        if exp <= now:
            del self._data[key]
            return None
        self._data.move_to_end(key)
        return value

    def __len__(self):
        now = time.time()
        return sum(1 for _, exp in self._data.values() if exp > now)
