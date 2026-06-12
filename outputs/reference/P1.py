import csv

def load_sales(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                if r.get("date") is None or r.get("city") is None or r.get("product") is None:
                    continue
                amount = float(r["amount"])
            except (TypeError, ValueError, KeyError):
                continue
            rows.append({"date": r["date"], "city": r["city"],
                         "product": r["product"], "amount": amount})
    return rows

def total_by_city(sales):
    out = {}
    for s in sales:
        out[s["city"]] = out.get(s["city"], 0.0) + s["amount"]
    return out

def top_product(sales):
    if not sales:
        return None
    totals = {}
    for s in sales:
        totals[s["product"]] = totals.get(s["product"], 0.0) + s["amount"]
    return max(totals, key=totals.get)
