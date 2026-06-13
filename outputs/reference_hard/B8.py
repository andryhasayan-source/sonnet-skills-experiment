from aiogram import Router

router = Router()

TRANSITIONS = {
    "new": {"paid", "cancelled"},
    "paid": {"shipped", "refunded"},
    "shipped": {"delivered"},
    "delivered": set(),
    "cancelled": set(),
    "refunded": set(),
}

class OrderFSM:
    def __init__(self):
        self._status = {}
        self._history = {}

    def _ensure(self, order_id):
        if order_id not in self._status:
            self._status[order_id] = "new"
            self._history[order_id] = ["new"]

    def status(self, order_id):
        self._ensure(order_id)
        return self._status[order_id]

    def can_transition(self, order_id, to_status):
        self._ensure(order_id)
        return to_status in TRANSITIONS.get(self._status[order_id], set())

    def transition(self, order_id, to_status):
        self._ensure(order_id)
        if to_status not in TRANSITIONS:
            return False
        if not self.can_transition(order_id, to_status):
            return False
        self._status[order_id] = to_status
        self._history[order_id].append(to_status)
        return True

    def history(self, order_id):
        self._ensure(order_id)
        return list(self._history[order_id])

    def is_terminal(self, order_id):
        self._ensure(order_id)
        return len(TRANSITIONS.get(self._status[order_id], set())) == 0

if __name__ == "__main__":
    pass
