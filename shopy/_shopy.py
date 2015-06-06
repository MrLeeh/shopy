"""
    Copyright 2015 by Stefan Lehmann
    
"""
import os
import time
import threading
from threading import Thread
from queue import Queue
from shopy.shop import Shop


class WorkerThread(Thread):
    def __init__(self, q: Queue,  shop: Shop, expression: str):
        super().__init__()
        self.queue = q
        self.shop = shop
        self.expression = expression
        self.result = None

    def run(self):
        self.result = self.shop.find(self.expression)
        self.queue.task_done()


class Shopy():
    def __init__(self):
        self.shops = []

    def find(self, expression):
        queue = Queue()
        threads = []
        for shop in self.shops:
            t = WorkerThread(queue, shop, expression)
            threads.append(t)
            t.start()
            queue.put((shop, expression))
        queue.join()

        for thread in threads:
            for item in thread.result:
                yield item


if __name__ == "__main__":
    o = Shopy()
    o.shops = [Shop.from_file('conrad'), Shop.from_file('rsonline')]

    for item in o.find('Batterien AAA 1.5V'):
        print(item)