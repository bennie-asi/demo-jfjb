# -*- coding:UTF-8 -*-
import datetime
from file.utils import MyFileUtil
from network.utils import jointURL
from network.request import request

todayDate = datetime.date.today()
yesterdayDate = (todayDate + datetime.timedelta(days=-1))
startDate = datetime.date(2022, 12, 1)
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


def getNews(newsUrl):
    '''传入新闻url，返回新闻标题与内容'''
    soup = request(newsUrl)
    res = {'title': '', 'content': ''}
    if soup:
        title = soup.find(id='APP-Title').string
        content = soup.find('founder-content').get_text()
        res['title'] = title
        res['content'] = content
    return res


def getSumUrl(baseURL):
    '''传入基础url获取所有的url'''
    res = dict()
    formate = '%Y-%m/%d'
    fDate = formatDate(todayDate, formate)
    # 生成当日所有版面URL
    for i in range(2, 14):
        after_url = 'node_%d.htm' % i
        nav_url = jointURL(baseUrl, fDate, after_url)
        # 存入对应版面的稿件URL
        newsUrls = getNewsURL(jointURL(baseUrl, fDate), nav_url)
        res[nav_url] = list(newsUrls)
    return res


def saveDocx(start: datetime, end=''):
    diff = (start - todayDate)
    if diff.days > 0:
        print('开始日期不能大于当日日期')
        start = todayDate
        # return
    if end:
        diff = (end - todayDate)
        if diff.days > 0:
            print('结束日期不能大于当日日期')
            end = todayDate
            # return
    diff1 = start - end
    if diff1.days > 0:
        print('开始日期不能大于结束日期')
        return
    detal = datetime.timedelta(days=1)
    while start <= end:

        start += detal


def userInput():
    separator = '='
    print(separator * 45)
    print(separator * 5 + '输入开始日期(必填）与截止日期(可选)例如：' + separator * 5)
    dateOperator = myFile.readYaml('config.yaml', 'config.dateOperator')
    print(separator * 12 + '2022-12-01' + dateOperator + '2022-12-01' + separator * 12)
    date = input('输入：').split(dateOperator)
    print(separator * 45)
    return date


if __name__ == '__main__':
    myFile = MyFileUtil()
    baseUrl = myFile.readYaml('config.yaml', 'config.baseURL')
    savePath = myFile.readYaml('config.yaml', 'config.savePath')

    suffix = myFile.readYaml('config.yaml', 'config.suffix')
    filename = str(startDate) + suffix
    path = myFile.getPath(filename, savePath)
    print("文档所在路径：%s" % path)

    # saveDocx(startDate)

    userInput()

    # sumUrl = getSumUrl(baseUrl)
    # for key, value in sumUrl.items():
    #     for newsUrl in value:
    #         news = getNews(newsUrl)
    #         myFile.writeDocx(path, title=news['title'], content=news['content'], date=startDate)
