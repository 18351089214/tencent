import json
import random
import time
from urllib.parse import urlencode

import redis
import requests
from config import *
from db import *
from requests.cookies import RequestsCookieJar
from selenium import webdriver

requests.packages.urllib3.disable_warnings()


class AutoPlay():
    def __init__(self):
        self.cookies_db = RedisClient('cookies', 'tencent')
        self.setr = redis.from_url(REDIS_URL)
        self.cookie_jar = RequestsCookieJar()
        str_cookies = self.cookies_db.get(QQ)
        dictCookies = json.loads(str_cookies)
        for i in range(0, len(dictCookies)):
            self.cookie_jar.set(dictCookies[i]['name'], dictCookies[i]['value'], domain=dictCookies[i]['domain'])

    def get_ip(self):
        try:
            resp = requests.get(IP_PROXY_URL)
            if resp.status_code == 200:
                ip = str(resp.content, encoding="utf8")
                return ip
            return None
        except Exception as e:
            print(e.args)
            return None

    # 返回一个随机的请求头 headers
    def get_headers(self):
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        ]
        UserAgent = random.choice(user_agent_list)
        headers = {'User-Agent': UserAgent}
        return headers

    def get_video_url(self):
        url = 'https://om.qq.com/mstatistic/VideoData/MediaVideoList?'
        for i in range(1, 108):
            params = {
                'limit': '8',
                'page': str(i),
                'fields': '2|3',
                'source': '0',
                'relogin': '1'
            }
            # url = base_url + urlencode(params)
            resp = requests.get(url=url, params=urlencode(params), headers=self.get_headers(), verify=False,
                                cookies=self.cookie_jar)

            if resp.status_code == 200:
                data = resp.json()
                items = data['data']['list']
                for item in items:
                    print(item['url'])
                    self.setr.sadd('tencent_urls', item['url'])

    def play_video(self):
        url = str(self.setr.srandmember('tencent_urls'))
        print(url)
        time.sleep(20)
        ip = self.get_ip()
        PROXY_PARAM = '--proxy-server=http://{}'.format(ip)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(PROXY_PARAM)
        chrome_options.add_argument('user-agent=%s' % self.get_headers())
        browser = webdriver.Chrome(chrome_options=chrome_options,
                                   executable_path=r'C:\ProgramData\Anaconda3\chromedriver.exe')
        browser.get(url)
        time.sleep(60)
        browser.quit()
        del browser

    def run(self):
        while True:
            self.play_video()


if __name__ == '__main__':
    obj = AutoPlay()
    # 用来获取播放URL，执行之前先取得Cookie
    obj.get_video_url()
    # obj.run()
