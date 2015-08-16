"""
    shop.py Copyright 2015 by Stefan Lehmann

"""

import os
import io
import requests
import logging
from lxml import html
from urllib.parse import urljoin
from requests.exceptions import MissingSchema

from shopy.shopitem import ShopItem
from shopy.utils import strip, fst, float_from_str, shop_path


logger = logging.getLogger('shopy.shop')


class InvalidSearchURL(Exception):
    pass


def log_parserror(shopname, itemnr, property):
    logger.debug(
        "Shop '%s', item %i: Could not parse '%s' property." %
        (shopname, itemnr, property)
    )


def shop_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'Shop':
        shop = Shop()
        shop.name = obj['name']
        shop.url = obj['url']
        shop.params = obj.get('params')
        shop.search_url = obj['search_url']
        shop.search_param = obj['search_param']
        shop.items = obj['items']
        return shop
    return obj


class Shop():

    def __init__(self):
        self.name = None
        self.url = None
        self.params = None
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
                raise FileNotFoundError(filename)

        with open(filename, 'r') as f:
            shop = Shop.from_json(f)

        return shop

    def find(self, search_term: str, timeout=10):
        payload = self.params if self.params is not None else {}
        payload[self.search_param] = search_term
        try:
            page = requests.get(
                self.search_url, params=payload, timeout=timeout)
            logger.debug(page.url)
        except MissingSchema as e:
            raise InvalidSearchURL(
                'Invalid search url "%s".' % self.search_url) from e
        return list(self.parse(page))

    def parse(self, page):
        tree = html.fromstring(page.text)
        try:
            container = tree.xpath(self.items['container']['xpath'])
        except KeyError:
            raise KeyError('items.container.xpath not defined')

        logger.debug("Found {} results".format(len(container)))

        for i, row in enumerate(container):
            item = ShopItem()
            item.shop = self

            # name
            if self._xpath('name'):
                try:
                    item.name = strip(fst(row.xpath(
                        self.items['name']['xpath']
                    )))
                except IndexError:
                    log_parserror(self.name, i, 'name')

            # articlenr
            if self._xpath('articlenr'):
                try:
                    item.articlenr = strip(fst(row.xpath(
                        self.items['articlenr']['xpath']
                    )))
                except IndexError:
                    log_parserror(self.name, i, 'articlenr')

            # price
            if self._xpath('price'):
                try:
                    item.price = float_from_str(strip(fst(row.xpath(
                        self.items['price']['xpath']
                    ))))
                except IndexError:
                    log_parserror(self.name, i, 'price')

            # url
            if self._xpath('url'):
                try:
                    item.url = strip(fst(
                        row.xpath(self.items['url']['xpath'])))
                    if self.items['url'].get('join') in (not None, True):
                        item.url = urljoin(self.url, item.url)
                except IndexError:
                    log_parserror(self.name, i, 'url')

            # images
            if self._xpath('images'):
                item.images = row.xpath(self.items['images']['xpath'])
                if self.items['images'].get('join') in (not None, True):
                    item.images = [urljoin(self.url, x) for x in item.images]

            if None not in (item.name, item.url):
                yield item
