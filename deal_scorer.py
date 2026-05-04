def calculate_profit(asking_price, estimated_resale_price, estimated_fees=0.0, estimated_transport=0.0):
    return estimated_resale_price - asking_price - estimated_fees - estimated_transport

def score_deal(listing):
    asking = float(listing.get("asking_price", 0) or 0)
    resale = float(listing.get("estimated_resale_price", 0) or 0)
    fees = float(listing.get("estimated_fees", 0) or 0)
    transport = float(listing.get("estimated_shipping_or_transport", 0) or 0)
    distance = listing.get("distance_miles")

    profit = calculate_profit(asking, resale, fees, transport)
    roi = profit / asking if asking > 0 else profit

    score = 0

    if profit >= 100:
        score += 40
    elif profit >= 50:
        score += 32
    elif profit >= 25:
        score += 22
    elif profit >= 10:
        score += 12

    if roi >= 3:
        score += 25
    elif roi >= 2:
        score += 20
    elif roi >= 1:
        score += 15
    elif roi >= 0.5:
        score += 8

    if asking == 0:
        score += 15
    elif asking <= 20:
        score += 10

    if distance is not None:
        d = float(distance)
        if d <= 5:
            score += 10
        elif d <= 15:
            score += 6
        elif d <= 30:
            score += 2
        else:
            score -= 10

    condition = str(listing.get("condition", "")).lower()
    if any(x in condition for x in ["new", "excellent", "like new"]):
        score += 10
    elif any(x in condition for x in ["broken", "for parts", "damaged"]):
        score -= 25

    score = max(0, min(100, round(score)))

    if score >= 80:
        recommendation = "hot"
    elif score >= 60:
        recommendation = "good"
    elif score >= 40:
        recommendation = "maybe"
    else:
        recommendation = "skip"

    return {
        "score": score,
        "recommendation": recommendation,
        "estimated_profit": round(profit, 2),
        "estimated_roi": round(roi, 2),
        "notes": {
            "hot": "Strong flip candidate. Message seller quickly and verify condition.",
            "good": "Good candidate if pickup is easy and condition checks out.",
            "maybe": "Only pursue if negotiation improves margin or pickup is very easy.",
            "skip": "Low margin or high risk. Skip unless you have a specific buyer."
        }[recommendation]
    }
