"""Replace these stubs with official marketplace/social API integrations."""

def send_customer_reply(platform: str, thread_id: str, message: str) -> dict:
    return {"sent": False, "reason": "stub_only", "platform": platform, "thread_id": thread_id, "message": message}

def publish_owned_social_post(platform: str, content: str) -> dict:
    return {"posted": False, "reason": "stub_only", "platform": platform, "content": content}

def update_listing_seo(platform: str, listing_id: str, title: str, description: str) -> dict:
    return {"updated": False, "reason": "stub_only", "platform": platform, "listing_id": listing_id}
