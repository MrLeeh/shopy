"""
    Copyright 2015 by Stefan Lehmann
    
"""


import pytest
from io import StringIO
from shopy.shop import Shop


simple_jsonstream = StringIO('{\n'
                     '  "__type__": "Shop",\n'
                     '  "name": "shop1",\n'
                     '  "url": "http://www.shop1.de",\n'
                     '  "search_url": "http://www.shop1.de/c",\n'
                     '  "search_param": "searchTerm"\n'
                     '}\n')


def test_from_json():
    shop = Shop.from_json(simple_jsonstream)
    assert shop.name == "shop1"
    assert shop.url == "http://www.shop1.de"

def test_wrongtype():
    stream = StringIO('{\n'
                     '  "__type__": "",\n'
                     '  "name": "shop1",\n'
                     '  "url": "http://www.shop1.de"\n'
                     '}\n')
    with pytest.raises(ValueError) as e:
        Shop.from_json(stream)
    assert "not of type 'Shop'" in str(e.value)

def test_corruptjson():
    stream = StringIO('{\n'
                     '  "__type__": "Shop"\n'
                     '  "name": "shop1",\n'
                     '  "url": "http://www.shop1.de"\n'
                     '}\n')
    with pytest.raises(ValueError) as e:
        Shop.from_json(stream)