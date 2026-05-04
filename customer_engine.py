from datetime import datetime, timedelta
from db.models import CustomerConversation, ConversationMessage, CustomerMemory, FollowUpTask, MessageArchive, Alert
from config import MAX_AUTO_FOLLOWUPS_PER_THREAD, REQUIRE_APPROVAL_FOR_ANGRY_CUSTOMERS

CATEGORIES = [
    "refund_request", "damaged_item", "missing_item", "shipping_issue",
    "address_change", "cancel_request", "product_question",
    "offer_negotiation", "general"
]

PRIORITY_MAP = {
    "refund_request": "urgent",
    "damaged_item": "urgent",
    "missing_item": "urgent",
    "shipping_issue": "high",
    "address_change": "high",
    "cancel_request": "high",
    "product_question": "medium",
    "offer_negotiation": "medium",
    "general": "low",
}

FOLLOW_UP_RULES_HOURS = {
    "waiting_for_photos": 24,
    "waiting_for_order_number": 24,
    "waiting_for_customer_response": 48,
    "post_resolution_checkin": 72,
}

def classify_message(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["refund", "money back", "return"]): return "refund_request"
    if any(w in t for w in ["broken", "damaged", "cracked", "arrived bad"]): return "damaged_item"
    if any(w in t for w in ["never arrived", "missing", "not delivered"]): return "missing_item"
    if any(w in t for w in ["tracking", "late", "shipping", "delay"]): return "shipping_issue"
    if any(w in t for w in ["address", "wrong address", "change my address"]): return "address_change"
    if any(w in t for w in ["cancel", "cancellation"]): return "cancel_request"
    if any(w in t for w in ["offer", "lower", "discount", "bundle"]): return "offer_negotiation"
    if "?" in t or any(w in t for w in ["size", "condition", "measure", "color"]): return "product_question"
    return "general"

def assign_priority(category: str, text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["chargeback", "scam", "report", "case", "angry", "unacceptable"]):
        return "urgent"
    return PRIORITY_MAP.get(category, "low")

def summarize_message(text: str) -> str:
    return text[:220] + ("..." if len(text) > 220 else "")

def generate_auto_reply(category: str, order_id: str | None = None) -> str:
    if category == "damaged_item":
        return "Hi, I’m sorry to hear there’s an issue with your item. Please send photos of the item, packaging, and your order number so we can review and help resolve this quickly."
    if category == "missing_item":
        return "Hi, thanks for reaching out. Please send your order number, and we’ll review the tracking details as quickly as possible."
    if category == "refund_request":
        return "Hi, thanks for the message. Please send your order number and a short description of the issue. We’ll review it and follow up shortly."
    if category == "shipping_issue":
        return "Hi, I can help check on this. Please send your order number and I’ll review the shipping status."
    if category == "product_question":
        return "Hi! Thanks for your question. Could you let us know exactly what you’d like to confirm about the item?"
    return "Hi! Thanks for reaching out. Please send any relevant details, such as your order number, item name, photos if needed, and what outcome you’re looking for."

def process_incoming_message(db, payload: dict) -> dict:
    platform = payload.get("platform", "unknown")
    customer_id = payload.get("customer_id", "unknown_customer")
    customer_name = payload.get("customer_name", "")
    thread_id = payload.get("thread_id") or f"{platform}:{customer_id}"
    order_id = payload.get("order_id", "")
    text = payload.get("message_text", "")

    category = classify_message(text)
    priority = assign_priority(category, text)
    summary = summarize_message(text)
    reply = generate_auto_reply(category, order_id)

    convo = db.query(CustomerConversation).filter_by(thread_id=thread_id).first()
    if not convo:
        convo = CustomerConversation(customer_id=customer_id, platform=platform, order_id=order_id, thread_id=thread_id, priority=priority)
        db.add(convo)
        db.flush()
    else:
        convo.last_message_at = datetime.utcnow()
        convo.priority = priority
        if order_id and not convo.order_id:
            convo.order_id = order_id

    msg = ConversationMessage(conversation_id=convo.id, sender="customer", message_text=text, ai_summary=summary, category=category, priority=priority)
    db.add(msg)
    db.flush()

    db.add(MessageArchive(platform=platform, customer_id=customer_id, customer_name=customer_name, order_id=order_id, thread_id=thread_id, sender="customer", message_text=text, ai_summary=summary, category=category, priority=priority))

    if priority in ["urgent", "high"]:
        db.add(Alert(message_id=msg.id, priority=priority, alert_text=f"{priority.upper()} customer message from {customer_name or customer_id}: {summary}"))

    followup_type = "waiting_for_order_number" if not order_id else "waiting_for_customer_response"
    hours = FOLLOW_UP_RULES_HOURS[followup_type]
    existing_followups = db.query(FollowUpTask).filter_by(conversation_id=convo.id).count()
    if existing_followups < MAX_AUTO_FOLLOWUPS_PER_THREAD:
        db.add(FollowUpTask(
            conversation_id=convo.id,
            customer_id=customer_id,
            platform=platform,
            follow_up_type=followup_type,
            scheduled_for=datetime.utcnow() + timedelta(hours=hours),
            message_text="Hi! Just checking in — when you have a chance, please send the requested details so we can help resolve this quickly."
        ))

    db.add(MessageArchive(platform=platform, customer_id=customer_id, customer_name=customer_name, order_id=order_id, thread_id=thread_id, sender="ai", message_text=reply, ai_summary="Automated intake reply", category=category, priority=priority, ai_reply_sent=True))
    db.commit()

    return {"category": category, "priority": priority, "summary": summary, "auto_reply": reply}
