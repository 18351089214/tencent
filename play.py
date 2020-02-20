# -*-*-
# 感谢骚男 『magic (QQ: 2191943283)』 提供的源代码
# 详细参考：https://www.jianshu.com/p/6b7f31a78f33
# -*-*-

import string
import sys
import time
import random
import zipfile
from multiprocessing.pool import Pool

import redis
from config import *
from db import *
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# setr = redis.from_url(REDIS_URL)
setr = redis.StrictRedis(host='47.96.88.67', port=6379, password='WF#pp034439', db=1)


def create_proxy_auth_extension(proxy_host, proxy_port,
                                proxy_username, proxy_password,
                                scheme='http', plugin_path=None):
    if plugin_path is None:
        plugin_path = r'./{}_{}@http-pro.abuyun.com_9010.zip'.format(proxy_username, proxy_password)

    manifest_json = """
       {
           "version": "1.0.0",
           "manifest_version": 2,
           "name": "Abuyun Proxy",
           "permissions": [
               "proxy",
               "tabs",
               "unlimitedStorage",
               "storage",
               "<all_urls>",
               "webRequest",
               "webRequestBlocking"
           ],
           "background": {
               "scripts": ["background.js"]
           },
           "minimum_chrome_version":"22.0.0"
       }
       """

    background_js = string.Template(
        """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
            }
          };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
        );
        """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path


def run(host, port, username, password):
    proxy_auth_plugin_path = create_proxy_auth_extension(
        proxy_host=host,
        proxy_port=port,
        proxy_username=username,
        proxy_password=password)
    url = str(setr.srandmember('weibo:urls'), encoding='utf-8')
    print(url)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--no-sandbox")
    chrome_options.add_extension(proxy_auth_plugin_path)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r'/usr/bin/chromedriver')
    wait = WebDriverWait(driver, timeout=10)
    if port != "9020":
        driver.get('http://proxy.abuyun.com/switch-ip')
    driver.get(url)
    # try:
    #     btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div.lite-page-wrap > div > div.main > div > article > div.weibo-rp > footer > div:nth-child(3) > i")))
    #     btn.click()
    # except Exception as e:
    #     print(e.args)
    time.sleep(random.random() * 5)
    driver.quit()
    del driver


if __name__ == '__main__':
    abuyun_conn = RedisClient('accounts', sys.argv[1])
    while True:
        p = Pool(2)
        try:
            key = str(abuyun_conn.usernames()[0])
            value = str(abuyun_conn.get(key))
            print(key)
            print(value)
            if sys.argv[1] == 'abuyunpro':
                host = 'http-pro.abuyun.com'
                port = '9010'
            elif sys.argv[1] == 'abuyundyn':
                host = 'http-dyn.abuyun.com'
                port = '9020'
            elif sys.argv[1] == 'abuyuncla':
                host = 'http-cla.abuyun.com'
                port = '9030'
            p.apply_async(run, args=(host, port, key, value))
            p.apply_async(run, args=(host, port, key, value))
            # p.apply_async(run, args=(host, port, key, value))
            # p.apply_async(run, args=(host, port, key, value))
            p.close()
            p.join()
        except Exception as e:
            print(e.args)
            time.sleep(10)
            continue
