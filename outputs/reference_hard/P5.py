class EventDeduplicator:
    def __init__(self, window_seconds):
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self.window = window_seconds
        self._seen = {}  # id -> last_time

    def _purge(self, now):
        dead = [k for k, t in self._seen.items() if now - t >= self.window]
        for k in dead:
            del self._seen[k]
        return len(dead)

    def is_duplicate(self, event_id, now):
        self._purge(now)
        dup = event_id in self._seen
        self._seen[event_id] = now  # обновляем свежесть в любом случае
        return dup

    def active_count(self, now):
        self._purge(now)
        return len(self._seen)

    def purge(self, now):
        return self._purge(now)
