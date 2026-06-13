from collections import OrderedDict
from aiogram import Router

router = Router()
PRICES = {"apple": 50, "bread": 40, "milk": 80}

class Cart:
    def __init__(self):
        self._carts = {}  # user_id -> OrderedDict(product -> qty)

    def _u(self, user_id):
        return self._carts.setdefault(user_id, OrderedDict())

    def add(self, user_id, product, qty=1):
        if qty <= 0:
            raise ValueError("qty must be > 0")
        c = self._u(user_id)
        c[product] = c.get(product, 0) + qty
        return c[product]

    def remove(self, user_id, product, qty=1):
        if qty <= 0:
            raise ValueError("qty must be > 0")
        c = self._u(user_id)
        if product not in c:
            return 0
        c[product] -= qty
        if c[product] <= 0:
            del c[product]
            return 0
        return c[product]

    def items(self, user_id):
        return dict(self._u(user_id))

    def total_qty(self, user_id):
        return sum(self._u(user_id).values())

    def clear(self, user_id):
        self._carts[user_id] = OrderedDict()

def cart_summary(cart, user_id):
    items = cart._u(user_id)
    if not items:
        return "Корзина пуста."
    lines, total = [], 0
    for product, qty in items.items():
        price = PRICES.get(product, 0)
        cost = price * qty
        total += cost
        lines.append(f"{product} x{qty} = {cost} руб.")
    lines.append(f"Итого: {total} руб.")
    return "\n".join(lines)

if __name__ == "__main__":
    pass
