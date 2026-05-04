"""
Marketplace router template.

Use this from your listing workflow when a human approves a draft.
"""

from typing import Dict, Any
from app.integrations.shopify_client import ShopifyClient
from app.integrations.ebay_client import EbayClient


def send_listing_to_platform(platform: str, listing: Dict[str, Any]) -> Dict[str, Any]:
    platform = platform.lower().strip()

    if platform == "shopify":
        client = ShopifyClient()
        return client.create_draft_product(
            title=listing["title"],
            body_html=listing.get("description", ""),
            price=str(listing.get("price", "0.00")),
            sku=listing.get("sku"),
            tags=listing.get("tags", []),
        )

    if platform == "ebay":
        client = EbayClient()
        return client.create_inventory_item_draft(
            sku=listing.get("sku", listing["title"].lower().replace(" ", "-")[:40]),
            title=listing["title"],
            description=listing.get("description", ""),
            price=str(listing.get("price", "0.00")),
        )

    return {"error": f"Unsupported platform: {platform}"}
