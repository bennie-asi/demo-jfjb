# -*- coding:UTF-8 -*-
import requests as rs
import time
import datetime
from bs4 import BeautifulSoup
from file.utils import MyFile

todayDate = datetime.date.today()
yesterdayDate = (todayDate + datetime.timedelta(days=-1))
startDate = todayDate
endDate = yesterdayDate

if __name__ == '__main__':
    myFile = MyFile()
    t = myFile.readYaml('config.yaml', 'config.baseURL')
    print('程序开始执行~')
    print(t)

