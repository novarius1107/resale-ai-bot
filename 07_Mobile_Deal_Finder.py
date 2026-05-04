import streamlit as st
import pandas as pd
from app.mobile_deal_finder.search_links import build_search_url
from app.mobile_deal_finder.deal_scorer import score_deal
from app.mobile_deal_finder.message_generator import generate_seller_message, generate_offer_message
from app.mobile_deal_finder.storage import load_saved_searches, save_search, load_listings, save_listing, update_listing_status

st.set_page_config(page_title="Mobile Deal Finder", layout="wide")

st.title("📱 Mobile Deal Finder")
st.caption("Phone-friendly tool for finding free and underpriced resale items without prohibited scraping.")

tab1, tab2, tab3, tab4 = st.tabs(["Saved Searches", "Import Listing", "Deal Pipeline", "Message Helper"])

with tab1:
    st.subheader("Saved search launchers")
    st.info("Tap a link from your phone to open Marketplace or Craigslist. Save promising listings manually back into this app.")

    searches = load_saved_searches()
    for s in searches:
        try:
            url = build_search_url(s["platform"], s["query"], s.get("max_price"))
            st.markdown(f"**{s.get('name', s['query'])}** — {s['platform']}  \n[Open search]({url})")
        except Exception as e:
            st.warning(f"Could not build URL for {s}: {e}")

    st.divider()
    st.subheader("Add new saved search")
    with st.form("add_search"):
        name = st.text_input("Search name", "Free furniture")
        platform = st.selectbox("Platform", ["craigslist", "facebook marketplace"])
        query = st.text_input("Search query", "free dresser")
        max_price = st.number_input("Max price", min_value=0.0, value=50.0, step=5.0)
        submitted = st.form_submit_button("Save search")
        if submitted:
            save_search({"name": name, "platform": platform, "query": query, "max_price": max_price})
            st.success("Saved search added. Refresh the page to see it.")

with tab2:
    st.subheader("Manually import a listing")
    st.caption("Copy/paste the listing details after you find something promising.")

    with st.form("import_listing"):
        title = st.text_input("Listing title")
        platform = st.selectbox("Platform", ["facebook marketplace", "craigslist", "other"])
        url = st.text_input("Listing URL")
        asking_price = st.number_input("Asking price", min_value=0.0, value=0.0, step=5.0)
        resale_price = st.number_input("Estimated resale price", min_value=0.0, value=100.0, step=5.0)
        transport = st.number_input("Estimated gas/transport cost", min_value=0.0, value=0.0, step=1.0)
        fees = st.number_input("Estimated platform fees", min_value=0.0, value=0.0, step=1.0)
        distance = st.number_input("Distance in miles", min_value=0.0, value=5.0, step=1.0)
        condition = st.selectbox("Condition", ["unknown", "new", "like new", "good", "fair", "damaged", "for parts"])
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Score and save")

        if submitted:
            listing = {
                "title": title,
                "platform": platform,
                "url": url,
                "asking_price": asking_price,
                "estimated_resale_price": resale_price,
                "estimated_shipping_or_transport": transport,
                "estimated_fees": fees,
                "distance_miles": distance,
                "condition": condition,
                "notes": notes,
                "status": "new",
            }
            result = score_deal(listing)
            listing["score_result"] = result
            listing["seller_message"] = generate_seller_message(title or "item", asking_price)
            save_listing(listing)
            st.success(f"Saved. Score: {result['score']} / 100 — {result['recommendation'].upper()}")
            st.write(result)

with tab3:
    st.subheader("Deal pipeline")
    listings = load_listings()
    if not listings:
        st.info("No listings saved yet.")
    else:
        flat = []
        for item in listings:
            score = item.get("score_result", {})
            flat.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "platform": item.get("platform"),
                "asking": item.get("asking_price"),
                "resale": item.get("estimated_resale_price"),
                "profit": score.get("estimated_profit"),
                "score": score.get("score"),
                "recommendation": score.get("recommendation"),
                "status": item.get("status"),
                "url": item.get("url"),
            })
        st.dataframe(pd.DataFrame(flat), use_container_width=True)

        st.divider()
        st.subheader("Update listing status")
        listing_id = st.number_input("Listing ID", min_value=1, step=1)
        status = st.selectbox("New status", ["new", "messaged", "scheduled pickup", "picked up", "listed for resale", "sold", "skipped"])
        if st.button("Update status"):
            update_listing_status(int(listing_id), status)
            st.success("Status updated.")

with tab4:
    st.subheader("Seller message helper")
    title = st.text_input("Item title", "dresser")
    asking = st.number_input("Asking price", min_value=0.0, value=0.0, step=5.0)
    pickup_time = st.text_input("Pickup time", "today")
    st.text_area("Simple message", generate_seller_message(title, asking, pickup_time), height=100)

    st.divider()
    offer = st.number_input("Offer price", min_value=0.0, value=max(0.0, asking * 0.75), step=5.0)
    st.text_area("Offer message", generate_offer_message(title, asking, offer, pickup_time), height=120)
