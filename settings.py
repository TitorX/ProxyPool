# coding=utf8
import os

# 服务密码
SERVER_PASSWD = os.environ.get('PROXY_POOL_PASSWD') or None

# 服务端口地址
SERVER_ADDR = ('0.0.0.0', 5454)

# 服务器返回的最大代理数
MAX_PROXIES = 100

# 获取代理的时间间隔 单位为秒
FETCH_INTERVAL = 120

# 测试代理池可用性的时间间隔 单位为秒
TEST_INTERVAL = 60

# 代理提取正则表达式
PROXY_REGX = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,4}"

# 采集超时时间
FETCH_TIMEOUT = 10

# 测试代理超时时间
TEST_TIMEOUT = 10

# 协程池大小
POOL_SIZE = 100

# 使用正则表达式进行代理采集的站点
RE_PROXY_SITES = []

# User-Agent
USER_AGENT_LIST = [
    'Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
    'Microsoft Internet Explorer/4.0b1 (Windows 95)',
    'Opera/8.00 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
]
