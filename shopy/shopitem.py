"""
    Copyright 2015 by Stefan Lehmann
    
"""


class ShopItem:
    def __init__(self):
        self.name = None
        self.articlenr = None
        self.price = None
        self.url = None
        self.images = []

    def __repr__(self):
        return "<ShopItem object name:'%s', articlenr:'%s', price:%0.2f>" % \
               (self.name,
                self.articlenr,
                self.price)