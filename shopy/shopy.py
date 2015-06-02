"""
    Copyright 2015 by Stefan Lehmann
    
"""

class Shopy():
    def __init__(self):
        self.shops = []

    def find(self, expression):
        return (shop.find(expression) for shop in self.shops)
