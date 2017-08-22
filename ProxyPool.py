# coding=utf-8
import time
import json

import gevent
from gevent.pool import Pool
from Fetcher import Fetcher
from functions import tester
from settings import FETCH_INTERVAL, POOL_SIZE, TEST_TIMEOUT, TEST_INTERVAL

FETCH_LIST = filter(lambda x: x.startswith('fetch_'), dir(Fetcher))


class ProxyPool:
    def __init__(self):
        self.fetcher = Fetcher()
        self.proxies_pool = set()
        self.init_pool()
        gevent.spawn(self.fetch_forever)
        gevent.spawn(self.test_forever)

    def init_pool(self):
        try:
            with open('proxies.json') as f:
                self.proxies_pool = set(json.load(f))
        except IOError:
            self.proxies_pool.update(self.fetcher.fetch())

    def test_forever(self):
        pool = Pool(POOL_SIZE)
        while True:
            proxies_pool = list(self.proxies_pool)
            print 'Start testing.'
            pool.map(self.test, proxies_pool)
            pool.join()
            with open('proxies.json', 'w+') as f:
                json.dump(proxies_pool, f)
            time.sleep(TEST_INTERVAL)

    def test(self, proxy):
        if not tester(proxy):
            try:
                self.proxies_pool.remove(proxy)
            except KeyError:
                pass

    def fetch_forever(self):
        while True:
            time.sleep(FETCH_INTERVAL)
            self.proxies_pool.update(self.fetcher.fetch())
