from urllib.parse import quote_plus

def facebook_marketplace_search_url(query, location_id="105702359464339", max_price=None):
    q = quote_plus(query)
    url = f"https://www.facebook.com/marketplace/{location_id}/search/?query={q}"
    if max_price is not None:
        url += f"&maxPrice={int(max_price)}"
    return url

def craigslist_search_url(query, city_subdomain="fairbanks", max_price=None):
    q = quote_plus(query)
    url = f"https://{city_subdomain}.craigslist.org/search/sss?query={q}&sort=date"
    if max_price is not None:
        url += f"&max_price={int(max_price)}"
    return url

def build_search_url(platform, query, max_price=None):
    platform = platform.lower().strip()
    if platform in ["facebook", "facebook marketplace", "marketplace"]:
        return facebook_marketplace_search_url(query, max_price=max_price)
    if platform in ["craigslist", "cl"]:
        return craigslist_search_url(query, max_price=max_price)
    raise ValueError(f"Unsupported platform: {platform}")
