import re

def mask_payment_info(text: str) -> str:
    text = re.sub(r"\b(?:\d[ -]*?){13,16}\b", "[masked_card]", text)
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[masked_ssn]", text)
    return text
