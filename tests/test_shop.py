"""
    Copyright 2015 by Stefan Lehmann
    
"""


import os
import pytest
from io import StringIO

import shopy
from shopy.shop import Shop, shop_path, InvalidSearchURL
from shopy.utils import fst

simple_json = ('{\n'
               '  "__type__": "Shop",\n'
               '  "name": "shop1",\n'
               '  "url": "http://www.shop1.de",\n'
               '  "search_url": "http://www.shop1.de/c",\n'
               '  "search_param": "searchTerm",\n'
               '  "items": {}'
               '}\n')


def test_from_json():
    shop = Shop.from_json(StringIO(simple_json))
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

def test_shops_directory():
    directory = shop_path()
    assert directory == os.path.join(fst(shopy.__path__), 'shops')

def test_filenotfound():
    with pytest.raises(FileNotFoundError) as e:
        Shop.from_file('wrongname')
    assert 'wrongname.json' in str(e.value)

def test_xpath_not_defined():
    shop = Shop.from_json(StringIO(simple_json))
    with pytest.raises(KeyError) as e:
        list(shop.find('search item'))
    assert 'items.container.xpath not defined' in str(e)

def test_invalid_searchurl():
    shop = Shop.from_json(StringIO(simple_json))
    shop.search_url = ''
    with pytest.raises(InvalidSearchURL) as e:
        shop.find('search item')
    assert 'Invalid search url' in str(e)
