"""
Shopify API connection template.

What this template supports:
- Reading products
- Creating draft products
- Updating inventory/title/description
- Keeping publishing disabled unless explicitly approved

Required .env:
SHOPIFY_STORE_DOMAIN
SHOPIFY_ADMIN_ACCESS_TOKEN
SHOPIFY_API_VERSION
AUTO_PUBLISH=false
"""

import os
import requests
from typing import Any, Dict, Optional


class ShopifyClient:
    def __init__(self) -> None:
        self.store_domain = os.getenv("SHOPIFY_STORE_DOMAIN", "")
        self.token = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN", "")
        self.api_version = os.getenv("SHOPIFY_API_VERSION", "2026-01")
        self.base_url = f"https://{self.store_domain}/admin/api/{self.api_version}"

    @property
    def enabled(self) -> bool:
        return bool(self.store_domain and self.token and self.token != "replace_me")

    def _headers(self) -> Dict[str, str]:
        return {
            "X-Shopify-Access-Token": self.token,
            "Content-Type": "application/json",
        }

    def list_products(self, limit: int = 50) -> Dict[str, Any]:
        if not self.enabled:
            return {"enabled": False, "products": []}

        url = f"{self.base_url}/products.json"
        response = requests.get(url, headers=self._headers(), params={"limit": limit}, timeout=30)
        response.raise_for_status()
        return response.json()

    def create_draft_product(
        self,
        title: str,
        body_html: str,
        price: str,
        sku: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> Dict[str, Any]:
        """
        Creates an unpublished product draft.
        Publishing should require human approval.
        """
        if not self.enabled:
            return {"enabled": False, "message": "Shopify credentials are not configured."}

        auto_publish = os.getenv("AUTO_PUBLISH", "false").lower() == "true"

        payload = {
            "product": {
                "title": title,
                "body_html": body_html,
                "status": "active" if auto_publish else "draft",
                "tags": ",".join(tags or []),
                "variants": [
                    {
                        "price": price,
                        "sku": sku or "",
                        "inventory_management": "shopify",
                    }
                ],
            }
        }

        url = f"{self.base_url}/products.json"
        response = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
