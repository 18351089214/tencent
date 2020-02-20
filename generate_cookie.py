import json
import time

import requests
from config import *
from db import *
from selenium import webdriver

requests.packages.urllib3.disable_warnings()


class QQShareFile(object):
    def __init__(self, website='penguinmedia'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument(PROXY_PARAM)
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options,
                                        executable_path=r'C:\ProgramData\Anaconda3\chromedriver.exe')
        self.browser.get('https://om.qq.com/userAuth/index')
        time.sleep(12)
        # 获取cookie
        dictCookies = self.browser.get_cookies()
        try:
            if self.cookies_db.set(QQ, json.dumps(dictCookies)):
                print('Cookie保存成功')
            else:
                print('Failed to save cookie!')
        except Exception as e:
            print(e.args)
        finally:
            self.browser.close()


if __name__ == '__main__':
    qq = QQShareFile()
    # qq.main()
