from db.models import MarketingOpportunity
from config import AUTO_POST_EXTERNAL_COMMUNITIES, REQUIRE_APPROVAL_FOR_PAID_ADS

def marketing_score(demand_score, margin_score, competition_score, trend_velocity):
    return round(demand_score * 0.4 + margin_score * 0.3 + competition_score * 0.2 + trend_velocity * 0.1, 2)

def recommend_platform(category: str):
    if category in ["apparel", "collectibles", "vintage"]:
        return "Instagram/TikTok owned account"
    if category in ["home", "decor"]:
        return "Pinterest + store SEO"
    return "Marketplace SEO + owned social"

def create_marketing_opportunity(db, product_name: str, category: str, demand=70, margin=70, competition=50, velocity=60):
    score = marketing_score(demand, margin, competition, velocity)
    platform = recommend_platform(category)
    auto_allowed = "owned" in platform.lower() or "seo" in platform.lower()
    rec = f"Promote {product_name} on {platform}. Use original photos, honest condition details, and product-specific keywords. External groups and paid ads require approval."
    opp = MarketingOpportunity(product_name=product_name, suggested_platform=platform, marketing_score=score, recommendation=rec, auto_action_allowed=auto_allowed)
    db.add(opp)
    db.commit()
    return opp
