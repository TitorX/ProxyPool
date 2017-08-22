# coding=utf-8
import time
import socket

import requests
from functools import wraps
from settings import TEST_TIMEOUT

def timer(func):
    """
    计时器装饰器
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print '{0} takes {1:.4f}s.'.format(func.__name__, end-start)
        return result
    return wrapper

def requests_exc(func):
    """
    处理requests请求出现的异常
    异常的请求返回False
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            requests.RequestException, requests.HTTPError,
            requests.packages.urllib3.exceptions.HTTPError,
            socket.error
        ) as e:
            return False
    return wrapper

@requests_exc
def get(*args, **kwargs):
    return requests.get(*args, **kwargs)

def tester(proxy):
    return get('http://baidu.com', proxies={'http': proxy}, timeout=TEST_TIMEOUT)
