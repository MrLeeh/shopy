"""
    Copyright 2015 by Stefan Lehmann
    
"""


from shopy import Shoplist, Shop

shoplist = Shoplist()
shoplist.shops = [
    Shop.from_file('conrad'),
    Shop.from_file('rsonline'),
    Shop.from_file('amazon')
]

for item in sorted(shoplist.find('Batterie AAA 1.5V'), key=lambda x: x.price):
    print(item)