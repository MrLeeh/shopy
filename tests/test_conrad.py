"""
    Copyright 2015 by Stefan Lehmann
    
"""
from shopy.shop import Shop

shop = Shop.load('conrad')

for item in shop.find("Batterien AAA 1.5V"):
    print(item, item.url, item.images)