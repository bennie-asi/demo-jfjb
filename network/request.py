import requests
from bs4 import BeautifulSoup


def request(url):
    '''传入一个url，返回一个通过lxml解析的bs4对象'''
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        print('请求失败~')
        return
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


if __name__ == '__main__':
    url = 'http://www.81.cn/jfjbmap/content/2022-12/30/content_330901.htm'
    url1 = 'http://www.81.cn/jfjbmap/content/2022-12/30/node_3.htm'
    soup = request(url)
    appTitle = soup.find(id='APP-Title').string
    appContent = soup.find('founder-content').get_text()
    print(appTitle)
    print(appContent)

