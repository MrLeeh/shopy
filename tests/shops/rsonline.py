"""
    Copyright 2015 by Stefan Lehmann
    
"""
from shopy.shop import Shop

with open('../shops/rsonline.json', 'r') as f:
    shop = Shop.from_json(f)

iterator = shop.find("Batterien AAA 1.5V")
for item in iterator:
    print(item, item.images)