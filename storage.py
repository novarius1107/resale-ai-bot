import json
import os

DATA_DIR = os.getenv("DATA_DIR", "data")
LISTINGS_FILE = os.path.join(DATA_DIR, "mobile_deal_listings.json")
SEARCHES_FILE = os.path.join(DATA_DIR, "mobile_saved_searches.json")

def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def _read_json(path, default):
    _ensure_data_dir()
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)

def _write_json(path, data):
    _ensure_data_dir()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_listings():
    return _read_json(LISTINGS_FILE, [])

def save_listing(listing):
    listings = load_listings()
    listing["id"] = len(listings) + 1
    listings.append(listing)
    _write_json(LISTINGS_FILE, listings)
    return listing

def update_listing_status(listing_id, status):
    listings = load_listings()
    found = False
    for item in listings:
        if int(item.get("id", 0)) == int(listing_id):
            item["status"] = status
            found = True
    _write_json(LISTINGS_FILE, listings)
    return found

def load_saved_searches():
    return _read_json(SEARCHES_FILE, [
        {"id": 1, "name": "Free stuff", "platform": "craigslist", "query": "free", "max_price": 0},
        {"id": 2, "name": "Moving sale", "platform": "craigslist", "query": "moving sale", "max_price": 50},
        {"id": 3, "name": "Tools", "platform": "craigslist", "query": "tools", "max_price": 50},
        {"id": 4, "name": "Carhartt", "platform": "facebook marketplace", "query": "Carhartt", "max_price": 60},
        {"id": 5, "name": "Dressers", "platform": "facebook marketplace", "query": "dresser", "max_price": 40}
    ])

def save_search(search):
    searches = load_saved_searches()
    search["id"] = len(searches) + 1
    searches.append(search)
    _write_json(SEARCHES_FILE, searches)
    return search
