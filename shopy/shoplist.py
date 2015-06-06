"""
    Copyright 2015 by Stefan Lehmann
    
"""


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


class Shoplist():
    def __init__(self):
        self.shops = []

    def find(self, expression):
        queue = Queue()
        threads = []
        for shop in self.shops:
            # start thread
            t = WorkerThread(queue, shop, expression)
            threads.append(t)
            t.start()
            # put in queue
            queue.put((shop, expression))

        # wait for all threads to finish
        queue.join()

        # yield found items
        for thread in threads:
            for item in thread.result:
                yield item