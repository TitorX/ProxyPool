# ProxyPool

从互联网上抓取可用的http代理，进行集中管理以及可用性测试，提供给爬虫类应用使用。


## 项目结构

```
Fetcher
    从不同来源抓取代理。
ProxyPool
    代理池，定期抓取代理、测试代理可用性。
Server
    提供用于获取代理的HTTP接口。
settings
    放置项目可配置项。
manager
    管理项目运行。
requirements
    项目依赖库列表。
```

## 使用说明

启动项目
```
python2 manager.py
```

获取代理列表，访问URL：
```
GET http://0.0.0.0:5454/
```

返回带有代理信息的JSON字符串
```
{
    'num': 1,  # 返回的代理数
    'proxies': [
        "http://117.135.250.134:82",
        ...  # 代理信息
    ],
    'status': 'Successful.',  # 请求成功
    'total': 292  # 代理池中代理总数
}
```

参数说明：

| name | explain | e.g. |
| :-: | :-: | :-: |
| num | 返回代理数(默认最大值100个，可在settings中更改) | num=10 |
| passwd | 服务密码(默认无密码，可在settings中更改) | passwd=test |
