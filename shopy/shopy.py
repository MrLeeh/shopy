"""
    Copyright 2015 by Stefan Lehmann
    
"""

import os


def shop_path():
    return os.path.join(os.path.dirname(__file__), 'shops')


class Shopy():
    def __init__(self):
        self.shops = []

    def find(self, expression):
        return (shop.find(expression) for shop in self.shops)
