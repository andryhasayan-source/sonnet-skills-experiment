import time

class RateLimiter:
    def __init__(self, max_calls, window_seconds):
        if max_calls < 1:
            raise ValueError("max_calls must be >= 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self.max_calls = max_calls
        self.window = window_seconds
        self._hits = {}

    def _cleanup(self, key, now):
        hits = self._hits.get(key, [])
        fresh = [t for t in hits if t > now - self.window]
        self._hits[key] = fresh
        return fresh

    def allow(self, key, now=None):
        now = time.time() if now is None else now
        fresh = self._cleanup(key, now)
        if len(fresh) + 1 <= self.max_calls:
            fresh.append(now)
            return True
        return False

    def remaining(self, key, now=None):
        now = time.time() if now is None else now
        fresh = self._cleanup(key, now)
        return max(0, self.max_calls - len(fresh))

    def reset(self, key):
        self._hits.pop(key, None)
