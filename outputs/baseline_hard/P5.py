class EventDeduplicator:
    def __init__(self, window_seconds: float):
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        self.window_seconds = window_seconds
        self._events = {}  # event_id -> last seen timestamp

    def _is_alive(self, t: float, now: float) -> bool:
        return now - t < self.window_seconds

    def is_duplicate(self, event_id: str, now: float) -> bool:
        self.purge(now)
        if event_id in self._events:
            self._events[event_id] = now
            return True
        self._events[event_id] = now
        return False

    def active_count(self, now: float) -> int:
        self.purge(now)
        return len(self._events)

    def purge(self, now: float) -> int:
        expired = [eid for eid, t in self._events.items() if not self._is_alive(t, now)]
        for eid in expired:
            del self._events[eid]
        return len(expired)