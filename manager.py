# coding=utf8
import gevent
from gevent.wsgi import WSGIServer
from gevent import monkey; monkey.patch_all()

from settings import SERVER_ADDR
from Server import proxy_pool, app

print 'Server starting: {0}'.format(SERVER_ADDR)
server = WSGIServer(SERVER_ADDR, app)
server.serve_forever()
