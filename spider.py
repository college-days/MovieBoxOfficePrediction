#This Python file uses the following encoding: utf-8
# __author__ = 'zjh'

import urllib2
import xlrd
import os
from BeautifulSoup import BeautifulSoup
import re
from time import sleep

def readExcelFunc():
    filesPath = os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')
    filePath = str(filesPath) + '/boxoffice.xls'

    data = xlrd.open_workbook(str(filePath))
    table = data.sheet_by_index(0)
    nrows = table.nrows
    movieNameList = []
    for rownum in range(1, nrows):
        movieNameList.append(table.row_values(rownum)[0])

    # for name in movieNameList:
    #     print name + "\n"
    simpleNameList = list(set(movieNameList))
    simpleNameList.sort(key=movieNameList.index)

    nameStrList = map(lambda str: str.encode('utf-8'), simpleNameList)

    return nameStrList

def generateDate():
    filesPath = os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')
    filePath = str(filesPath) + '/movie_view.xls'
    boxFilePath = str(filesPath) + '/boxoffice.xls'

    data = xlrd.open_workbook(str(filePath))
    table = data.sheet_by_index(2)
    # table = data.sheet_by_index(0)
    nrows = table.nrows
    # print nrows

    boxData = xlrd.open_workbook(str(boxFilePath))
    boxTable = boxData.sheet_by_index(0)
    boxnrows = boxTable.nrows
    boxMovieName = []
    filterName = []
    for rownum in range(1, boxnrows):
        boxMovieName.append(boxTable.row_values(rownum)[0].encode('utf-8'))

    filterName = list(set(boxMovieName))
    filterName.sort(key=boxMovieName.index)

    movieMap = {}
    for rownum in range(1, nrows):
        movieName = table.row_values(rownum)[1].encode('utf-8')
        # movieName = str(table.row_values(rownum)[0].encode('gbk'))
        # print type(movieName)
        if movieName in filterName:
            movieDate = table.row_values(rownum)[9].encode('utf-8')
            movieMap[movieName] = movieDate

    movieDateMap = {}
    # movieDict = [lambda value: value.replace('-', '') for value in movieMap.values()]
    for key, value in movieMap.items():
        # print key + '--->' + value + '\n'
        valueList = str(value).split('-')
        valueIntList = map(lambda value: int(value), valueList)
        # print valueIntList
        dataSum = valueIntList[0]*12 + valueIntList[1]
        newSum = dataSum-4
        year = newSum / 12
        month = newSum % 12
        oldDate = str(year) + '-' + str(month) + '-' + str(valueIntList[2])
        newDate = value

        finalDate = oldDate + ':' + newDate

        movieDateMap[key] = finalDate

    for key, value in movieDateMap.items():
        print 'key===>' + str(key) + 'value===>' + str(value)

    print len(movieDateMap)

    return movieDateMap

def simpleSpider(url):
    # proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    # urllib2.install_opener(opener)

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')

    response = urllib2.urlopen(request)
    the_page = response.read()

    cleaSoup = BeautifulSoup(the_page)

    scripts = cleaSoup.findAll('script')

    rp = re.compile(r'W_textc(.*?)span')
    result = rp.findall(str(scripts))

    try:
        newResult = result[-1]
        print newResult
        rp = re.compile(r' (.*?) ')
        clea = rp.findall(newResult)
        print clea
        newClea = map(lambda item: item.replace(',', ''), clea)
        finalResult = int(newClea[0])
        print 'finalResult===>' + str(finalResult)
        return finalResult
    except IndexError:
        print 'this url is something bad ' + str(url)
        return 1


def movieSpider():
    movieNameList = readExcelFunc()
    movieDateMap = generateDate()

    proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    movieMap = {}
    for movieName in movieNameList:
        url = 'http://s.weibo.com/weibo/' + str(movieName) + '&timescope=custom:' + movieDateMap[str(movieName)] + '&Refer=g'
# http://s.weibo.com/weibo/searchcontent&timescope=custom:2012-10-02:2013-01-01&Refer=g

        finalResult = 0

        requestCounter = 0

        #有时候爬下来是0 要重新爬取但又不能无限制 所以设置一个10次的次数
        while True:
            print 'looping'
            requestCounter += 1
            if requestCounter > 10:
                finalResult = 3
                break

            print movieName
            try:
                finalResult = simpleSpider(url)
            except:
                proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
                urllib2.install_opener(opener)

            if int(finalResult) != 0:
                break

        print type(finalResult)
        print 'final result' + str(finalResult)

        movieMap[movieName] = finalResult
        sleep(3)

    print movieMap
    # saveFile(movieMap)

    file = open(str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalweibo.txt', 'a')
    for key, value in movieMap.items():
        file.write(str(key) + '-' + str(value) + '\n')
    file.close()

if __name__ == '__main__':
    # movieSpider()
    # urlStr = 'http://s.weibo.com/weibo/%E6%B3%B0%E5%9B%A7&timescope=custom:2012-8-12:2012-12-12&Refer=g'
    # simpleSpider(urlStr)
    # movieSpider()
    file = open(str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalweibo.txt', 'r')
    data = file.readlines()
    print len(data)
    file.close()