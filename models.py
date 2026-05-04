from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from db.session import Base

class TrendingItem(Base):
    __tablename__ = "trending_items"
    id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    category = Column(String, default="general")
    source = Column(String, default="manual/mock")
    trend_score = Column(Float, default=0)
    avg_sold_price = Column(Float, default=0)
    estimated_cost = Column(Float, default=0)
    estimated_profit = Column(Float, default=0)
    risk_level = Column(String, default="low")
    source_url = Column(String, default="")
    status = Column(String, default="review")
    created_at = Column(DateTime, default=datetime.utcnow)

class DraftListing(Base):
    __tablename__ = "draft_listings"
    id = Column(Integer, primary_key=True)
    trending_item_id = Column(Integer, ForeignKey("trending_items.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    platform = Column(String, default="eBay")
    suggested_price = Column(Float, default=0)
    shipping_price = Column(Float, default=0)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)

class CustomerConversation(Base):
    __tablename__ = "customer_conversations"
    id = Column(Integer, primary_key=True)
    customer_id = Column(String, nullable=False)
    platform = Column(String, default="unknown")
    order_id = Column(String, default="")
    thread_id = Column(String, index=True, nullable=False)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    current_status = Column(String, default="open")
    priority = Column(String, default="low")
    created_at = Column(DateTime, default=datetime.utcnow)

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("customer_conversations.id"))
    sender = Column(String, nullable=False)
    message_text = Column(Text, nullable=False)
    ai_summary = Column(Text, default="")
    category = Column(String, default="general")
    priority = Column(String, default="low")
    created_at = Column(DateTime, default=datetime.utcnow)

class CustomerMemory(Base):
    __tablename__ = "customer_memory"
    id = Column(Integer, primary_key=True)
    customer_id = Column(String, unique=True, nullable=False)
    known_preferences = Column(Text, default="")
    past_issues = Column(Text, default="")
    open_orders = Column(Text, default="")
    previous_refunds = Column(Text, default="")
    notes = Column(Text, default="")
    updated_at = Column(DateTime, default=datetime.utcnow)

class FollowUpTask(Base):
    __tablename__ = "follow_up_tasks"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("customer_conversations.id"))
    customer_id = Column(String, nullable=False)
    platform = Column(String, default="unknown")
    follow_up_type = Column(String, default="waiting_for_customer_response")
    scheduled_for = Column(DateTime, nullable=False)
    message_text = Column(Text, nullable=False)
    status = Column(String, default="scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)

class MessageArchive(Base):
    __tablename__ = "message_archive"
    id = Column(Integer, primary_key=True)
    platform = Column(String, default="unknown")
    customer_id = Column(String, default="")
    customer_name = Column(String, default="")
    order_id = Column(String, default="")
    thread_id = Column(String, default="")
    sender = Column(String, default="customer")
    message_text = Column(Text, nullable=False)
    ai_summary = Column(Text, default="")
    category = Column(String, default="general")
    priority = Column(String, default="low")
    ai_reply_sent = Column(Boolean, default=False)
    human_reply_sent = Column(Boolean, default=False)
    attachments = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, nullable=True)
    priority = Column(String, default="low")
    alert_text = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MarketingOpportunity(Base):
    __tablename__ = "marketing_opportunities"
    id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    suggested_platform = Column(String, default="owned_social")
    marketing_score = Column(Float, default=0)
    recommendation = Column(Text, default="")
    auto_action_allowed = Column(Boolean, default=False)
    status = Column(String, default="review")
    created_at = Column(DateTime, default=datetime.utcnow)
