import requests

base = "http://127.0.0.1:8000"
print(requests.get(base + "/").json())
print(requests.post(base + "/webhooks/customer-message", json={
    "platform": "eBay",
    "customer_id": "buyer_123",
    "customer_name": "Demo Buyer",
    "message_text": "My item arrived damaged. Can I get a refund?"
}).json())
print(requests.post(base + "/trend/candidate", json={
    "product_name": "Vintage Adidas Track Jacket",
    "category": "apparel",
    "avg_sold_price": 54.99,
    "estimated_cost": 18.00,
    "source": "demo"
}).json())
