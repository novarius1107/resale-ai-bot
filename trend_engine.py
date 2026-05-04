from db.models import TrendingItem, DraftListing

RESTRICTED_KEYWORDS = ["weapon", "gun", "ammo", "counterfeit", "replica", "prescription", "recalled"]

def risk_filter(product_name: str) -> str:
    t = product_name.lower()
    if any(k in t for k in RESTRICTED_KEYWORDS):
        return "blocked"
    if any(k in t for k in ["nike", "designer", "luxury", "apple"]):
        return "medium"
    return "low"

def estimate_profit(avg_sold_price: float, estimated_cost: float, shipping: float = 8.99, fee_rate: float = 0.13) -> float:
    fees = avg_sold_price * fee_rate
    return round(avg_sold_price - estimated_cost - shipping - fees, 2)

def generate_draft_listing(product_name: str, category: str, price: float) -> dict:
    return {
        "title": f"{product_name} - Clean Condition - Fast Shipping",
        "description": "AI draft: verify photos, measurements, authenticity, condition, and platform policy before publishing.",
        "suggested_price": price,
        "shipping_price": 8.99,
    }

def add_trending_candidate(db, product_name: str, category: str, avg_sold_price: float, estimated_cost: float, source="manual"):
    risk = risk_filter(product_name)
    profit = estimate_profit(avg_sold_price, estimated_cost)
    status = "blocked" if risk == "blocked" else "review"
    item = TrendingItem(product_name=product_name, category=category, source=source, trend_score=70, avg_sold_price=avg_sold_price, estimated_cost=estimated_cost, estimated_profit=profit, risk_level=risk, status=status)
    db.add(item)
    db.flush()
    if status != "blocked":
        draft = generate_draft_listing(product_name, category, avg_sold_price)
        db.add(DraftListing(trending_item_id=item.id, title=draft["title"], description=draft["description"], suggested_price=draft["suggested_price"], shipping_price=draft["shipping_price"]))
    db.commit()
    return item
