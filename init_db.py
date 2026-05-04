from db.session import engine, SessionLocal
from db.models import Base, TrendingItem, DraftListing, MarketingOpportunity

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    if db.query(TrendingItem).count() == 0:
        sample = TrendingItem(
            product_name="Vintage Nike Windbreaker",
            category="apparel",
            source="demo",
            trend_score=86,
            avg_sold_price=64.99,
            estimated_cost=22.00,
            estimated_profit=28.50,
            risk_level="medium",
            source_url="https://example.com/demo"
        )
        db.add(sample)
        db.flush()
        db.add(DraftListing(
            trending_item_id=sample.id,
            title="Vintage Nike Windbreaker Jacket - Clean Condition",
            description="Draft listing generated from trend engine. Confirm condition, size, photos, and measurements before publishing.",
            platform="eBay",
            suggested_price=64.99,
            shipping_price=8.99
        ))
        db.add(MarketingOpportunity(
            product_name="Vintage Nike Windbreaker",
            suggested_platform="Instagram/TikTok owned account",
            marketing_score=82,
            recommendation="Post a short video showing condition, tag, logo, and styling. Use resale and vintage streetwear keywords.",
            auto_action_allowed=True
        ))
        db.commit()
finally:
    db.close()
print("Database initialized.")
