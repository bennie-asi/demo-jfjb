# -*- coding:UTF-8 -*-
import datetime
from file.utils import MyFileUtil
from network.utils import jointURL
from network.request import request

todayDate = datetime.date.today()
yesterdayDate = (todayDate + datetime.timedelta(days=-1))
startDate = todayDate
endDate = yesterdayDate


def formatDate(date: datetime, formate='%Y-%m-%d'):
    return date.strftime(formate)


def getNewsURL(tempUrl, navURL):
    '''传入版面URL返回稿件的URL列表'''
    soup = request(navURL)
    res = list()
    if soup:
        a_tags = soup.find(id='APP-NewsList').find_all('a')
        for a in a_tags:
            # print(a.get('href'))
            res.append(tempUrl + a.get('href'))
    # print(res)
    return res


def getNewsContent(newsUrl):
    '''传入新闻url，返回新闻标题与内容'''
    soup = request(newsUrl)
    res = {'title': '', 'content': ''}
    if soup:
        title = soup.find(id='APP-Title').string
        content = soup.find('founder-content').get_text()
        res['title'] = title
        res['content'] = content
    return res


if __name__ == '__main__':
    myFile = MyFileUtil()
    baseUrl = myFile.readYaml('config.yaml', 'config.baseURL')
    savePath = myFile.readYaml('config.yaml', 'config.savePath')

    formate = '%Y-%m/%d'
    fDate = formatDate(todayDate, formate)

    # 生成当日所有版面URL
    sumURL = dict()
    for i in range(2, 14):
        after_url = 'node_%d.htm' % i
        nav_url = jointURL(baseUrl, fDate, after_url)
        # 存入对应版面的稿件URL
        newsUrls = getNewsURL(jointURL(baseUrl, fDate), nav_url)
        sumURL[nav_url] = list(newsUrls)

    suffix = myFile.readYaml('config.yaml', 'config.suffix')
    filename = str(todayDate) + suffix
    path = myFile.newFile(filename, savePath)
    print(path)
