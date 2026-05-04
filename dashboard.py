import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
from db.session import SessionLocal, engine
from db.models import Base, TrendingItem, DraftListing, CustomerConversation, ConversationMessage, FollowUpTask, MessageArchive, Alert, MarketingOpportunity
from engines.customer_engine import process_incoming_message
from engines.trend_engine import add_trending_candidate
from engines.marketing_engine import create_marketing_opportunity

Base.metadata.create_all(bind=engine)
st.set_page_config(page_title="Resale AI Store Bot", layout="wide")
st.title("Resale AI Store Bot")
st.caption("Semi-autonomous resale dashboard with approval gates.")

def rows_to_df(rows):
    return pd.DataFrame([{c.name: getattr(r, c.name) for c in r.__table__.columns} for r in rows])

db = SessionLocal()
try:
    page = st.sidebar.radio("Navigation", ["Overview", "Trending Items", "Draft Listings", "Customer Inbox", "Follow-Ups", "Message Archive", "Marketing", "Alerts", "Demo Tools"])

    if page == "Overview":
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Trending Items", db.query(TrendingItem).count())
        c2.metric("Draft Listings", db.query(DraftListing).count())
        c3.metric("Open Conversations", db.query(CustomerConversation).filter(CustomerConversation.current_status == "open").count())
        c4.metric("Unread Alerts", db.query(Alert).filter(Alert.is_read == False).count())
        st.info("Safety defaults are enabled: no auto-buying, no auto-publishing, no refunds, no paid ads without approval.")

    elif page == "Trending Items":
        st.subheader("Trending Items")
        rows = db.query(TrendingItem).order_by(TrendingItem.created_at.desc()).all()
        st.dataframe(rows_to_df(rows), use_container_width=True)

    elif page == "Draft Listings":
        st.subheader("Draft Listings")
        rows = db.query(DraftListing).order_by(DraftListing.created_at.desc()).all()
        st.dataframe(rows_to_df(rows), use_container_width=True)
        st.warning("Publishing is intentionally not automated. Review every listing before posting.")

    elif page == "Customer Inbox":
        st.subheader("Customer Inbox")
        convos = db.query(CustomerConversation).order_by(CustomerConversation.last_message_at.desc()).all()
        for c in convos:
            with st.expander(f"{c.priority.upper()} | {c.platform} | {c.customer_id} | Order: {c.order_id or 'n/a'}"):
                msgs = db.query(ConversationMessage).filter_by(conversation_id=c.id).order_by(ConversationMessage.created_at).all()
                for m in msgs:
                    st.markdown(f"**{m.sender}** — {m.created_at}  \n{m.message_text}")
                    st.caption(f"Category: {m.category} | Priority: {m.priority} | Summary: {m.ai_summary}")

    elif page == "Follow-Ups":
        st.subheader("Scheduled Follow-Ups")
        rows = db.query(FollowUpTask).order_by(FollowUpTask.scheduled_for.asc()).all()
        st.dataframe(rows_to_df(rows), use_container_width=True)

    elif page == "Message Archive":
        st.subheader("Message Archive")
        q = st.text_input("Search archive")
        rows = db.query(MessageArchive).order_by(MessageArchive.created_at.desc()).all()
        df = rows_to_df(rows)
        if q and not df.empty:
            mask = df.astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
            df = df[mask]
        st.dataframe(df, use_container_width=True)
        if not df.empty:
            st.download_button("Export CSV", df.to_csv(index=False), "message_archive.csv", "text/csv")

    elif page == "Marketing":
        st.subheader("Marketing Opportunities")
        rows = db.query(MarketingOpportunity).order_by(MarketingOpportunity.marketing_score.desc()).all()
        st.dataframe(rows_to_df(rows), use_container_width=True)
        st.info("Auto actions are limited to owned channels/listing SEO. Paid ads, outreach, and external communities require approval.")

    elif page == "Alerts":
        st.subheader("Alerts")
        rows = db.query(Alert).order_by(Alert.created_at.desc()).all()
        st.dataframe(rows_to_df(rows), use_container_width=True)

    elif page == "Demo Tools":
        st.subheader("Create Demo Customer Message")
        with st.form("demo_msg"):
            platform = st.text_input("Platform", "eBay")
            customer_id = st.text_input("Customer ID", "buyer_123")
            customer_name = st.text_input("Customer name", "Demo Buyer")
            order_id = st.text_input("Order ID", "")
            message_text = st.text_area("Message", "My item arrived damaged. Can I get a refund?")
            submitted = st.form_submit_button("Process message")
        if submitted:
            result = process_incoming_message(db, {"platform": platform, "customer_id": customer_id, "customer_name": customer_name, "order_id": order_id, "message_text": message_text})
            st.success(result)

        st.subheader("Add Demo Trending Item")
        with st.form("demo_trend"):
            product_name = st.text_input("Product", "Vintage Adidas Track Jacket")
            category = st.text_input("Category", "apparel")
            avg_sold_price = st.number_input("Average sold price", value=54.99)
            estimated_cost = st.number_input("Estimated cost", value=18.00)
            submitted2 = st.form_submit_button("Add candidate")
        if submitted2:
            item = add_trending_candidate(db, product_name, category, avg_sold_price, estimated_cost, source="dashboard_demo")
            create_marketing_opportunity(db, product_name, category)
            st.success(f"Added item #{item.id} with risk {item.risk_level} and profit ${item.estimated_profit}")
finally:
    db.close()
