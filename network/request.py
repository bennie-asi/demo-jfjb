import requests
from bs4 import BeautifulSoup


def request(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    headers = {'User-Agent': user_agent}
    res = requests.get(url, headers=headers)
    if res.status_code == requests.codes.ok:
        print('请求成功~')
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'lxml')
    return res


if __name__ == '__main__':
    url = 'http://www.81.cn/jfjbmap/content/2022-12/29/content_330837.htm'
    url1 = 'http://www.81.cn/jfjbmap/content/2022-12/29/node_3.htm'
    res = request(url)
    print(res.text)
