import time
from collections import deque


class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: float):
        if max_calls < 1:
            raise ValueError("max_calls must be >= 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._history = {}

    def _purge(self, key: str, now: float):
        dq = self._history.get(key)
        if dq is None:
            return None
        cutoff = now - self.window_seconds
        while dq and dq[0] <= cutoff:
            dq.popleft()
        if not dq:
            del self._history[key]
            return None
        return dq

    def allow(self, key: str, now: float = None) -> bool:
        if now is None:
            now = time.time()
        dq = self._history.get(key)
        if dq is None:
            dq = deque()
            self._history[key] = dq
        dq = self._purge(key, now)
        if dq is None:
            dq = deque()
            self._history[key] = dq

        if len(dq) < self.max_calls:
            dq.append(now)
            return True
        return False

    def remaining(self, key: str, now: float = None) -> int:
        if now is None:
            now = time.time()
        dq = self._purge(key, now)
        used = len(dq) if dq is not None else 0
        return max(0, self.max_calls - used)

    def reset(self, key: str) -> None:
        self._history.pop(key, None)