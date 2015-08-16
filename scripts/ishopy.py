#!/usr/bin/env python
"""
    shopy-find.py Copyright 2015 by stefanlehmann

"""

import sys
import re
import logging

import webbrowser
from tabulate import tabulate

sys.path.insert(0, '..')
from shopy.shop import Shop
from shopy.utils import iter_shops, green
from shopy import Shoplist


HEADERS = ('nr', 'name', 'price', 'shop')


def sort_by_price(x):
    return x.price or 0.


def limit_str(s):
    return s[:50]


def item_rows(items):
    return [
        (i, limit_str(item.name), "{:8.2f}€".format(item.price or 0.),
            item.shop.name) for (i, item) in enumerate(items, 1)
    ]


# init logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('shopy')
logger.setLevel(logging.WARNING)


while True:
    cmd = input(green("> "))

    # print table
    if cmd.startswith("find"):
        # get searchterm
        re_res = (
            re.search('^find "(.*)"', cmd)
            or re.search('^find (.*)$', cmd)
        )
        if re_res is not None:
            searchterm = re_res.group(1)
        else:
            continue

        # get shoplist
        shoplist = Shoplist()
        re_res = re.search(' on (.*)$', cmd)
        if re_res is None:
            shoplist.shops = [Shop.from_file(f) for f in iter_shops()]
        else:
            shopnames = list(map(
                lambda x: x.strip(), re_res.group(1).split(',')))
            shoplist.shops = [Shop.from_file(f) for f in shopnames]

        print(green("\nLooking for \"{}\" on {}\n".format(
            searchterm, [s.name for s in shoplist.shops])))

        # create list of items
        items = sorted(shoplist.find(searchterm), key=sort_by_price)
        print(tabulate(item_rows(items), headers=HEADERS))

    elif cmd == "show":
        print(tabulate(item_rows(items), headers=HEADERS))

    elif cmd.startswith("show"):
        shops = [s.lower() for s in cmd.split()[1:]]
        rows = item_rows([i for i in items if i.shop.name.lower() in shops])
        print(tabulate(rows, headers=HEADERS))

    elif cmd.startswith("open"):
        for i in map(int, cmd.split()[1:]):
            item = items[i-1]
            webbrowser.open(item.url, new=2)

    elif cmd == "shoplist":
        for i, s in enumerate([Shop.from_file(f) for f in iter_shops()], 1):
            print("[{}] {}".format(i, s.name))

    elif cmd in ("quit", "q"):
        break
