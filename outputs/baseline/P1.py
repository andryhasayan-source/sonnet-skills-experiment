import csv


def load_sales(path: str) -> list[dict]:
    sales = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = row["date"]
                city = row["city"]
                product = row["product"]
                amount = float(row["amount"])
            except (KeyError, TypeError, ValueError):
                continue
            sales.append({
                "date": date,
                "city": city,
                "product": product,
                "amount": amount,
            })
    return sales


def total_by_city(sales: list[dict]) -> dict:
    result = {}
    for sale in sales:
        city = sale["city"]
        result[city] = result.get(city, 0.0) + sale["amount"]
    return result


def top_product(sales: list[dict]) -> str | None:
    totals = {}
    for sale in sales:
        product = sale["product"]
        totals[product] = totals.get(product, 0.0) + sale["amount"]
    if not totals:
        return None
    return max(totals, key=totals.get)