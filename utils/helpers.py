import re


def parse_price(text):
    return float(re.sub(r"[^\d.]", "", text))
