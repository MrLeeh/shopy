"""
    Copyright 2015 by Stefan Lehmann
    
"""
from shopy.shop import Shop

shop = Shop.from_file('amazon')

for item in shop.find("Batterien AAA 1.5V"):
    print(item, item.url, item.images)