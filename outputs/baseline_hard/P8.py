class TokenBucket:
    EPS = 1e-9

    def __init__(self, capacity: float, refill_rate: float):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        if refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self._last = None

    def _refill(self, now: float):
        if self._last is None:
            self._last = now
            return
        dt = now - self._last
        if dt > 0:
            self.tokens = min(self.capacity, self.tokens + dt * self.refill_rate)
        self._last = now

    def consume(self, tokens: float, now: float) -> bool:
        if tokens <= 0:
            raise ValueError("tokens must be > 0")
        self._refill(now)
        if tokens > self.capacity + self.EPS:
            return False
        if self.tokens + self.EPS >= tokens:
            self.tokens -= tokens
            if self.tokens < 0:
                self.tokens = 0
            return True
        return False

    def available(self, now: float) -> float:
        self._refill(now)
        return self.tokens