"""
    test_shopitem.py Copyright 2015 by stefanlehmann
    
"""

import pytest
from shopy.shop import Shop
from shopy.shopitem import ShopItem


def test_shopitem_repr():
	
    shop = Shop.from_file('amazon.json')
    item = ShopItem()
    item.name = "testitem"
    item.articlenr = "123"
    item.price = 12.5
    item.shop = shop
    assert repr(item) == \
           "<ShopItem object (name:'%s', articlenr:'%s'," \
           " price:%s, shop:'%s')>" % (
               'testitem',
               '123',
               '12.50',
               'Amazon'
           )
