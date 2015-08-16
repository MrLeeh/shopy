"""
    shoplist.py Copyright 2015 by Stefan Lehmann

"""

import time
from threading import Thread
from queue import Queue

from .utils import green


THREAD_COUNT = 5


def download_shopitems(q, res_q):
    while not q.empty():
        shop, expression = q.get()

        # measure time of searching the shop
        t0 = time.clock()
        result = shop.find(expression)
        t1 = time.clock()
        timespan = t1 - t0

        res_q.put((shop, timespan, result))
        q.task_done()


class Shoplist():

    def __init__(self):
        self.shops = []

    def find(self, expression):
        queue = Queue()
        res_queue = Queue()

        # put in queue
        for shop in self.shops:
            queue.put((shop, expression))

        for i in range(5):
            worker = Thread(
                target=download_shopitems, args=(queue, res_queue)
            )
            worker.start()

        # wait for all threads to finish
        items = []
        while queue.unfinished_tasks:
            shop, timespan, res = res_queue.get()
            print(green("{}: found {} items in {:.0f} ms".format(
                shop.name, len(res), timespan * 1000.)))
            items += res

        # yield found items
        for item in items:
            yield item
