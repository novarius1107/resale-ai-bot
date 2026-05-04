from fastapi import APIRouter
from app.mobile_deal_finder.storage import load_listings, save_listing, update_listing_status, load_saved_searches, save_search
from app.mobile_deal_finder.deal_scorer import score_deal
from app.mobile_deal_finder.search_links import build_search_url
from app.mobile_deal_finder.message_generator import generate_seller_message, generate_offer_message

router = APIRouter(prefix="/mobile-deals", tags=["mobile-deals"])

@router.get("/searches")
def get_searches():
    searches = load_saved_searches()
    for search in searches:
        search["url"] = build_search_url(search["platform"], search["query"], search.get("max_price"))
    return searches

@router.post("/searches")
def create_search(search: dict):
    saved = save_search(search)
    saved["url"] = build_search_url(saved["platform"], saved["query"], saved.get("max_price"))
    return saved

@router.get("/listings")
def get_listings():
    return load_listings()

@router.post("/listings")
def create_listing(listing: dict):
    listing["score_result"] = score_deal(listing)
    listing["seller_message"] = generate_seller_message(
        title=listing.get("title", "item"),
        asking_price=float(listing.get("asking_price", 0) or 0),
    )
    return save_listing(listing)

@router.post("/listings/{listing_id}/status")
def set_listing_status(listing_id: int, payload: dict):
    return {"updated": update_listing_status(listing_id, payload.get("status", "new"))}

@router.post("/message/offer")
def create_offer_message(payload: dict):
    return {
        "message": generate_offer_message(
            title=payload.get("title", "item"),
            asking_price=float(payload.get("asking_price", 0) or 0),
            offer_price=float(payload.get("offer_price", 0) or 0),
            pickup_time=payload.get("pickup_time", "today"),
        )
    }
