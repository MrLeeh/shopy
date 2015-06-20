"""
    shopitem.py Copyright 2015 by Stefan Lehmann
    
"""


class ShopItem:
    def __init__(self):
        self.name = None
        self.articlenr = None
        self.price = None
        self.url = None
        self.shop = None
        self.images = []

    def __repr__(self):
        return "<ShopItem object (name:'%s', articlenr:'%s', price:%s, " \
               "shop:'%s')>" % \
               (self.name,
                self.articlenr,
                "%0.2f" % self.price if self.price is not None else None,
                self.shop.name)