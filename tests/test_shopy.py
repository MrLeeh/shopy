"""
    Copyright 2015 by Stefan Lehmann
    
"""
from pprint import pprint

from shopy import Shoplist, Shop

shoplist = Shoplist()
shoplist.shops = [
    Shop.from_file('amazon'),
    Shop.from_file('ebay')
]

searchterm = "Bernhard Cornwell Sharpe"
iterator = sorted(shoplist.find(searchterm), key=lambda x: x.price)
for item in iterator:
    pprint((item.name, "%0.2f" % item.price))