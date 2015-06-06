"""
    shopy - shop.py
    Copyright 2015 by Stefan Lehmann

"""

import os
import io
import requests
from lxml import html
from urllib.parse import urljoin

from shopy.shopitem import ShopItem
from shopy.utils import strip, fst, float_from_str, shop_path


def shop_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'Shop':
        shop = Shop()
        shop.name = obj['name']
        shop.url = obj['url']
        shop.search_url = obj['search_url']
        shop.search_param = obj['search_param']
        shop.items = obj['items']
        return shop
    return obj


class Shop():
    def __init__(self):
        self.name = None
        self.url = None
        self.search_url = None
        self.search_param = None

    def _xpath(self, name):
        return name in self.items and 'xpath' in self.items['name']

    @staticmethod
    def from_json(stream: io.IOBase) -> 'Shop':
        import json
        shop = json.load(stream, object_hook=shop_decoder)
        if not isinstance(shop, Shop):
            raise ValueError("Json object is not of type 'Shop'")
        return shop

    @staticmethod
    def from_file(shopname)->'Shop':

        # is shopname a valid filename?
        if os.path.isfile(shopname):
            filename = shopname
        else:
            # look in the common shops directory
            filename = os.path.join(
                shop_path(),
                shopname if shopname.endswith('.json') else shopname + '.json')

            if not os.path.isfile(filename):
                raise FileNotFoundError()

        with open(filename, 'r') as f:
            shop = Shop.from_json(f)

        return shop

    def find(self, search_term: str):
        payload = {self.search_param: search_term}
        page = requests.get(self.search_url, params=payload)
        return self.parse(page)

    def parse(self, page):
        tree = html.fromstring(page.text)
        try:
            container = tree.xpath(self.items['container']['xpath'])
        except KeyError as e:
            raise KeyError('items.container.xpath not defined')

        for row in container:
            item = ShopItem()
            item.shop = self
            # name
            if self._xpath('name'):
                item.name = strip(fst(row.xpath(
                    self.items['name']['xpath']
                )))

            # articlenr
            if self._xpath('articlenr'):
                item.articlenr = strip(fst(row.xpath(
                    self.items['articlenr']['xpath']
                )))

            # price
            if self._xpath('price'):
                item.price = float_from_str(strip(fst(row.xpath(
                    self.items['price']['xpath']
                ))))

            # url
            if self._xpath('url'):
                item.url = strip(fst(row.xpath(self.items['url']['xpath'])))
                if self.items['url'].get('join') in (not None, True):
                    item.url =  urljoin(self.url, item.url)

            # images
            if self._xpath('images'):
                item.images = row.xpath(self.items['images']['xpath'])
                if self.items['images'].get('join') in (not None, True):
                    item.images = [urljoin(self.url, x) for x in item.images]

            yield item
