import random
import time

from selenium import webdriver


def get_headers():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://10.110.8.54:8080')
chrome_options.add_argument('user-agent=%s' % get_headers())
chrome_options.add_argument('--headless')
# 下面这行解决崩溃问题 也可能是driver和chrome不匹配
chrome_options.add_argument('''--no-sandbox''')
# 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('''--disable-gpu''')
browser = webdriver.Chrome(chrome_options=chrome_options,
                           executable_path=r'C:\ProgramData\Anaconda3\chromedriver.exe')

if __name__ == '__main__':
    browser.get('http://v.qq.com/page/113/119/51/q0528m187w3.html')
    browser.maximize_window()
    for i in range(10):
        picture_url = browser.save_screenshot('%s.png' % str(i))
        time.sleep(5)
    browser.close()
