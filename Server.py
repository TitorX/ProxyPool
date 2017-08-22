# coding=utf-8
import os
import random
from flask import Flask, request, jsonify

from settings import SERVER_ADDR, MAX_PROXIES, SERVER_PASSWD
from ProxyPool import ProxyPool

proxy_pool = ProxyPool()

app = Flask(__name__)

@app.route('/')
def handle():
    passwd = request.args.get('passwd', None)
    if passwd != SERVER_PASSWD:
        return jsonify({'status': 'Incorrect password.'})
    num = int(request.args.get('num', 1))
    num = num if num>=0 else 0
    num = num if num<=100 else 100
    num = num if num<=len(proxy_pool.proxies_pool) else len(proxy_pool.proxies_pool)
    result = random.sample(proxy_pool.proxies_pool, num)
    return jsonify({'status': 'Successful.', 'num': num, 'total': len(proxy_pool.proxies_pool), 'proxies': result})
