from aiogram import Router

router = Router()

class Dispatcher:
    def __init__(self):
        self._ops = []                 # порядок добавления
        self._load = {}                # op_id -> set(ticket_id)
        self._assigned = {}            # ticket_id -> op_id

    def add_operator(self, op_id):
        if op_id not in self._load:
            self._ops.append(op_id)
            self._load[op_id] = set()

    def remove_operator(self, op_id):
        if op_id not in self._load:
            return []
        tickets = list(self._load[op_id])
        for t in tickets:
            self._assigned.pop(t, None)
        del self._load[op_id]
        self._ops.remove(op_id)
        return tickets

    def assign(self, ticket_id):
        if ticket_id in self._assigned:
            return self._assigned[ticket_id]
        if not self._ops:
            return None
        # наименее загруженный, при равенстве — раньше добавленный
        best = min(self._ops, key=lambda op: (len(self._load[op]),
                                              self._ops.index(op)))
        self._load[best].add(ticket_id)
        self._assigned[ticket_id] = best
        return best

    def close(self, ticket_id):
        if ticket_id not in self._assigned:
            return False
        op = self._assigned.pop(ticket_id)
        self._load[op].discard(ticket_id)
        return True

    def load(self, op_id):
        return len(self._load.get(op_id, ()))

if __name__ == "__main__":
    pass
