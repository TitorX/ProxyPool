# coding=utf-8
import random
import re
import time
from functools import wraps

import gevent
from gevent.pool import Pool
from lxml import html
from functions import get, tester, timer
from settings import (
    USER_AGENT_LIST, FETCH_TIMEOUT, PROXY_REGX, TEST_TIMEOUT, POOL_SIZE,
    RE_PROXY_SITES,
)

get_ua = lambda: random.choice(USER_AGENT_LIST)


class Fetcher:
    """
    代理采集器
    """

    def __init__(self):
        self.FETCH_LIST = filter(lambda x: x.startswith('fetch_'), dir(self))
        self.proxies_list = []
        self.filted_proxies = set()
        self.test_pool = Pool(POOL_SIZE)

    def fetch(self):
        print 'Start fetching.'
        self.proxies_list = []
        self.filted_proxies = set()
        pool = Pool(POOL_SIZE)
        pool.map(self.call_fetch, self.FETCH_LIST)
        pool.join()
        self.test_fetching()
        print 'Fetch {0} valid proxies.'.format(len(self.filted_proxies))
        return self.filted_proxies

    def call_fetch(self, fetch_func):
        proxies = getattr(self, fetch_func)()
        print '{0} fetch {1} proxies.'.format(fetch_func, len(proxies))
        self.proxies_list.extend(proxies)

    @timer
    def test_fetching(self):
        """
        对返回的代理列表进行可用性测试
        过滤掉无效的、重复的代理
        """
        proxies_list = set(self.proxies_list)
        self.test_pool.map(self._tester, proxies_list)
        self.test_pool.join()

    def _tester(self, proxy):
        if tester(proxy):
            self.filted_proxies.add(proxy)

    @timer
    def fetch_re(self):
        """
        基于正则代理采集
        """
        proxies = []
        for site in RE_PROXY_SITES:
            response = get(site, headers={'User-Agent': get_ua()}, timeout=FETCH_TIMEOUT)
            if response:
                res = re.findall(PROXY_REGX, response.text)
                proxies.extend(res)

        return map(lambda ip: 'http://' + ip, proxies)

    # @timer
    # def fetch_xici(self):
    #     """
    #     从西刺网站采集代理
    #     """
    #     URLS = ['http://www.xicidaili.com/nn/{0}'.format(i) for i in range(1, 6)]
    #     proxies = []
    #     for url in URLS:
    #         r = get(url, headers={'User-Agent': get_ua()}, timeout=FETCH_TIMEOUT)
    #         if r:
    #             response = html.fromstring(r.text)
    #             for line in response.cssselect('#ip_list')[0].xpath('tr')[1:]:
    #                 try:
    #                     proxy = ':'.join(map(lambda x: x.xpath('text()')[0], line.xpath('td')[1:3]))
    #                     proxies.append(proxy)
    #                 except IndexError:
    #                     pass
    #     return map(lambda ip: 'http://' + ip, proxies)

    @timer
    def fetch_kdl(self):
        """
        快代理
        """
        URLS = ['http://www.kuaidaili.com/free/inha/{0}'.format(i) for i in range(1, 6)]
        proxies = []
        for url in URLS:
            res = get(url, headers={'User-Agent': get_ua()}, timeout=FETCH_TIMEOUT)
            if res:
                try:
                    res = html.fromstring(res.text)
                    res = res.xpath("//tbody//tr//td[@data-title='IP' or @data-title='PORT']/text()")
                    res = map(lambda ip,port: ':'.join([ip, port]), res[::2], res[1::2])
                    proxies.extend(res)
                except IndexError:
                    pass
        return map(lambda ip: 'http://' + ip, proxies)
