"""
    shopy - shop.py
    Copyright 2015 by Stefan Lehmann

"""


class Shop():
    def __init__(self):
        self.name = ""


def from_json(json_dict):
    def try_get(prop, default=""):
        try:
            return json_dict[prop]
        except KeyError:
            return default

    newshop = Shop()
    newshop.name = try_get("name")
    newshop.website = try_get("website")
    return newshop
