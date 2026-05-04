def generate_seller_message(title, asking_price, pickup_time="today"):
    if float(asking_price or 0) <= 0:
        return f"Hi, is this still available? I can pick it up {pickup_time} if that works. Thanks!"
    return f"Hi, is this still available? I’m interested in the {title}. Would you be able to do a quick pickup {pickup_time}? Thanks!"

def generate_offer_message(title, asking_price, offer_price, pickup_time="today"):
    return f"Hi, is this still available? I’m interested in the {title}. Would you consider ${offer_price:.0f} if I can pick it up {pickup_time}? Thanks!"
