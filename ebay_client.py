"""
eBay API connection template.

What this template supports:
- Placeholder OAuth setup
- Creating listing drafts only
- Keeping publish/list actions disabled unless explicitly approved

Required .env:
EBAY_ENV=sandbox
EBAY_CLIENT_ID
EBAY_CLIENT_SECRET
EBAY_REFRESH_TOKEN
EBAY_MARKETPLACE_ID=EBAY_US
AUTO_PUBLISH=false

Note:
Actual eBay listing publication requires completing OAuth, account policies,
shipping/payment/return policy IDs, category IDs, and marketplace compliance checks.
"""

import os
import base64
import requests
from typing import Any, Dict


class EbayClient:
    def __init__(self) -> None:
        self.env = os.getenv("EBAY_ENV", "sandbox")
        self.client_id = os.getenv("EBAY_CLIENT_ID", "")
        self.client_secret = os.getenv("EBAY_CLIENT_SECRET", "")
        self.refresh_token = os.getenv("EBAY_REFRESH_TOKEN", "")
        self.marketplace_id = os.getenv("EBAY_MARKETPLACE_ID", "EBAY_US")

        if self.env == "production":
            self.api_base = "https://api.ebay.com"
        else:
            self.api_base = "https://api.sandbox.ebay.com"

    @property
    def enabled(self) -> bool:
        return all([
            self.client_id and self.client_id != "replace_me",
            self.client_secret and self.client_secret != "replace_me",
            self.refresh_token and self.refresh_token != "replace_me",
        ])

    def get_access_token(self) -> str:
        if not self.enabled:
            raise RuntimeError("eBay credentials are not configured.")

        credentials = f"{self.client_id}:{self.client_secret}".encode()
        auth_header = base64.b64encode(credentials).decode()

        url = f"{self.api_base}/identity/v1/oauth2/token"
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "scope": "https://api.ebay.com/oauth/api_scope/sell.inventory",
        }

        response = requests.post(url, headers=headers, data=data, timeout=30)
        response.raise_for_status()
        return response.json()["access_token"]

    def create_inventory_item_draft(self, sku: str, title: str, description: str, price: str) -> Dict[str, Any]:
        """
        Creates or updates an inventory item draft-like record.
        This does not publish an offer unless a separate approved publish function is added.
        """
        if not self.enabled:
            return {"enabled": False, "message": "eBay credentials are not configured."}

        token = self.get_access_token()
        url = f"{self.api_base}/sell/inventory/v1/inventory_item/{sku}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Content-Language": "en-US",
            "X-EBAY-C-MARKETPLACE-ID": self.marketplace_id,
        }

        payload = {
            "availability": {
                "shipToLocationAvailability": {
                    "quantity": 1
                }
            },
            "condition": "USED_GOOD",
            "product": {
                "title": title[:80],
                "description": description,
                "aspects": {},
                "imageUrls": []
            }
        }

        response = requests.put(url, headers=headers, json=payload, timeout=30)
        if response.status_code not in (200, 201, 204):
            response.raise_for_status()

        return {
            "status": "draft_inventory_item_saved",
            "sku": sku,
            "auto_publish": os.getenv("AUTO_PUBLISH", "false").lower() == "true",
            "note": "Offer publishing is intentionally not automated in this template."
        }
