class TokenBucket:
    EPS = 1e-9
    def __init__(self, capacity, refill_rate):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        if refill_rate < 0:
            raise ValueError("refill_rate must be >= 0")
        self.capacity = float(capacity)
        self.rate = float(refill_rate)
        self.tokens = float(capacity)
        self._last = None

    def _refill(self, now):
        if self._last is None:
            self._last = now
            return
        dt = now - self._last
        if dt > 0:
            self.tokens = min(self.capacity, self.tokens + dt * self.rate)
            self._last = now

    def consume(self, tokens, now):
        if tokens <= 0:
            raise ValueError("tokens must be > 0")
        self._refill(now)
        if tokens > self.capacity + self.EPS:
            return False
        if self.tokens + self.EPS >= tokens:
            self.tokens = max(0.0, self.tokens - tokens)
            return True
        return False

    def available(self, now):
        self._refill(now)
        return self.tokens
