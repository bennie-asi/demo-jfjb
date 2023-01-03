# -*- coding:UTF-8 -*-
import datetime, time
from file.utils import MyFileUtil
from network.utils import jointURL
from network.request import request

todayDate = datetime.date.today()
yesterdayDate = (todayDate + datetime.timedelta(days=-1))


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
        title = soup.find(id='APP-Title').get_text()
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
    # for i in range(2, 14):
    #     after_url = 'node_%d.htm' % i
    #     nav_url = jointURL(baseUrl, fDate, after_url)
    #     # 存入对应版面的稿件URL
    #     newsUrls = getNewsURL(jointURL(baseUrl, fDate), nav_url)
    #     res[nav_url] = list(newsUrls)

    # 版面URL通过node_2来获取
    after_url = 'node_2.htm'
    nav_url_2 = jointURL(baseURL, fDate, after_url)

    soup = request(nav_url_2)
    a_tags = soup.find(id='section-list-xs').find_all('a')
    for a in a_tags:
        after_url = a.get('href')
        nav_url = jointURL(baseUrl, fDate, after_url)
        newsUrls = getNewsURL(jointURL(baseUrl, fDate), nav_url)
        res[nav_url] = list(newsUrls)
    # print('getSumURl', res)
    return res


def saveDocx(path, baseUrl, start, end=None):
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
    else:
        end = start
    diff1 = start - end
    if diff1.days > 0:
        print('开始日期不能大于结束日期')
        return
    detal = datetime.timedelta(days=1)
    sumUrl = getSumUrl(baseUrl)
    while start <= end:
        myFile = MyFileUtil()
        for key, value in sumUrl.items():
            for newsUrl in value:
                news = getNews(newsUrl)
                # print(news['title'])
                myFile.writeDocx(path, title=news['title'], content=news['content'], date=start)
        start += detal


def userInput():
    from inputimeout import inputimeout, TimeoutOccurred
    myFile = MyFileUtil()
    separator = '='
    print(''.center(50, separator))
    print('输入开始日期(必填）与截止日期(可选)例如：'.center(50, separator))
    dateOperator = myFile.readYaml('config.yaml', 'config.dateOperator')
    timeout = myFile.readYaml('config.yaml', 'config.timeout')
    print(str('2022-12-29' + dateOperator + '2022-12-30').center(50, separator))
    date = list()
    try:
        print(str('你有%d秒钟的时间来输入，超时自动输入今日日期' % timeout).center(50, separator))
        date.extend(inputimeout(prompt='>>', timeout=timeout).strip().split(dateOperator))
    except TimeoutOccurred:
        print('超时自动输入~')
        date.append(str(todayDate))
        # date.extend('2022-12-29~2022-12-30'.split(dateOperator))
    # date = input('输入：').split(dateOperator)
    print(''.center(50, separator))
    return date


if __name__ == '__main__':
    myFile = MyFileUtil()

    baseUrl = myFile.readYaml('config.yaml', 'config.baseURL')
    savePath = myFile.readYaml('config.yaml', 'config.savePath')
    suffix = myFile.readYaml('config.yaml', 'config.suffix')
    formate = myFile.readYaml('config.yaml', 'config.dateFormat')

    # startDate = todayDate
    endDate = todayDate

    data = userInput()
    # print(date)
    filename = '~'.join(data) + suffix
    path = myFile.getPath(filename, savePath)
    print("文档所在路径：%s" % path)
    try:
        startDate = datetime.datetime.strptime(data[0].strip(), formate).date()
    except Exception as e:
        print(e)
        print('输入的数据格式不正确,5秒后程序将退出')
        time.sleep(5)
    date_len = len(data)
    if date_len == 1:
        saveDocx(path=path, baseUrl=baseUrl, start=startDate)
    if date_len == 2:
        endDate = datetime.datetime.strptime(data[1].strip(), formate).date()
        saveDocx(path=path, baseUrl=baseUrl, start=startDate, end=endDate)
    print('程序执行完成，3秒后程序将退出')
    time.sleep(3)
