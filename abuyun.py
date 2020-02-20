# -*-*-
# 感谢骚男 『│網亊隨楓︵ (QQ: 332110637)』 提供的源代码
# -*-*-

import sys
import time
# ! -*- encoding:utf-8 -*-
from datetime import datetime
from urllib import request

import redis
from config import *
from db import *

setr = redis.from_url(REDIS_URL)

# 要访问的目标页面
targetUrl = "http://test.abuyun.com"
# targetUrl = "http://proxy.abuyun.com/switch-ip"
# targetUrl = "http://proxy.abuyun.com/current-ip"

# 代理服务器
proxyHost = "http-pro.abuyun.com"
proxyPort = "9010"

# 代理隧道验证信息
proxyUser = "HMI3Q27T9H99N17P"
proxyPass = "C6966BD30DA47B37"


def run(proxy_handler, port):
    # auth = request.HTTPBasicAuthHandler()
    # opener = request.build_opener(proxy_handler, auth, request.HTTPHandler)

    opener = request.build_opener(proxy_handler)
    if port != "9020":
        opener.addheaders = [("Proxy-Switch-Ip", "yes")]
    request.install_opener(opener)
    url = str(setr.srandmember('tencent_urls'), encoding='utf-8')
    print(url)
    resp = request.urlopen(url).read()


if __name__ == '__main__':
    abuyun_conn = RedisClient('accounts', sys.argv[1])
    begin_date = datetime.now()
    # p = Pool(5)
    while True:
        end_date = datetime.now()
        result = ((end_date - begin_date).seconds) / 3600
        try:
            key = str(abuyun_conn.usernames()[0], encoding="utf-8")
            value = str(abuyun_conn.get(key), encoding='utf-8')
            host = ''
            port = ''
            if sys.argv[1] == 'abuyunpro':
                host = 'http-pro.abuyun.com'
                port = '9010'
            elif sys.argv[1] == 'abuyundyn':
                host = 'http-dyn.abuyun.com'
                port = '9020'
            elif sys.argv[1] == 'abuyuncla':
                host = 'http-cla.abuyun.com'
                port = '9030'

            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host": host,
                "port": port,
                "user": key,
                "pass": value,
            }

            proxy_handler = request.ProxyHandler({
                "http": proxyMeta,
                "https": proxyMeta,
            })
            run(proxy_handler, port)
        except Exception as e:
            print(e.args)
            time.sleep(10)
            continue
