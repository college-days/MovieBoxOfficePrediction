#This Python file uses the following encoding: utf-8
# __author__ = 'zjh'
import urllib2
import os
import xlrd
from BeautifulSoup import BeautifulSoup
import re
from time import sleep
import sys

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

def simpleParseStarring(url):
    # urlString = 'http://www.m1905.com/search/?type=film&q=楼'
    # proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    # urllib2.install_opener(opener)

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')

    response = urllib2.urlopen(request)
    the_page = response.read()

    cleaSoup = BeautifulSoup(the_page)

    lis = cleaSoup.findAll('li', attrs={
        "class":"star"
        })

    starrings = lis[0].findAll('a', attrs={
        "class": "text-box-new"
        })

    for starring in starrings:
        print starring.string

    names = [name.string for name in starrings]

    # movieStarring = u'楼'+ '-' + ','.join(names)

    movieStarring = ','.join(names)

    print movieStarring

    return movieStarring

def parseStarring():
# urlString = 'http://www.m1905.com/search/?type=film&q=楼'
    movieNames = readExcelFunc()

    proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    movieStarringMap = {}
    for moviename in movieNames:
        url = 'http://www.m1905.com/search/?type=film&q=' + moviename
        try:

            movieStarringString = simpleParseStarring(url)
            movieStarringMap[moviename] = movieStarringString

        except:
            print str(moviename) + '---has some problem'
            movieStarringMap[moviename] = ''
            proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)

        sleep(3)


    file = open(str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/moviestarringnames.txt', 'a')

    for key, value in movieStarringMap.items():
        try:
            file.write(str(key) + '-' + str(value) + '\n')
        except:
            print str(key) + '--->has some write in problem'
    file.close()

def simpleParseNews(url):
    # urlString = 'http://news.baidu.com/ns?from=news&cl=2&bt=1344700800&y0=2012&m0=8&d0=12&y1=2012&m1=12&d1=12&et=1355241600&q1=人再囧途之泰囧&submit=百度一下&q3=&q4=&mt=0&lm=&s=2&begin_date=2012-8-12&end_date=2012-12-12&tn=newstitledy&ct=0&rn=20&q6='
    proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')

    response = urllib2.urlopen(request)
    the_page = response.read()

    cleaSoup = BeautifulSoup(the_page)

    tds = cleaSoup.findAll('td', attrs={
        "align": "right",
        "nowrap": "nowrap"
        })

    # tdstring = str(tds)
    # tdSplits = tdstring.split('\n')
    # news = int(tdSplits[1].strip())
    # # print news
    # return news

    tdstring = str(tds)
    print type(tdstring)
    tdSplits = tdstring.split('\n')
    tdfinalString = tdSplits[1].strip()


    print tdfinalString

    pattern = re.compile(r'\d+')

    results = pattern.findall(tdfinalString)

    print type(results)

    rank = len(results)-1

    totalnews = 0
    for i in range(0, len(results)):
        totalnews = totalnews + int(results[i])*(1000**(rank-i))

    # print totalnews
    return totalnews


def generateNewsUrlMills(times):
    # 2012-04-12:1334160000

    begintime = times[0]
    endtime = times[1]

    resulttimes = {}

    begintimes = begintime.split('-')

    # print begintimes
    if begintimes[0] == '2012':
        resulttimes['begin'] = int(1334160000 + ((int(begintimes[1])-4)*30.5+int(begintimes[2])-12)*24*60*60)
    elif begintimes[0] == '2013':
        resulttimes['begin'] = int(1334160000 + ((int(begintimes[1])+8)*30.5+int(begintimes[2])-12)*24*60*60)

    endtimes = endtime.split('-')

    # print endtimes
    if endtimes[0] == '2012':
        resulttimes['end'] = int(1334160000 + ((int(endtimes[1])-4)*30.5+int(endtimes[2])-12)*24*60*60)
    elif endtimes[0] == '2013':
        resulttimes['end'] = int(1334160000 + ((int(endtimes[1])+8)*30.5+int(endtimes[2])-12)*24*60*60)

    return resulttimes

def parseNews():
    movieNamesList = readExcelFunc()
    movieDateMap = generateDate()

    proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    movieNewsMap = {}
    for moviename in movieNamesList:
        # if moviename in movieDateMap:
        #     print str(moviename) + '===>' + str(movieDateMap[moviename])
        movieDate = movieDateMap[moviename]
        movieDates = movieDate.split(':')
        begintime = movieDates[0]
        endtime = movieDates[1]

        begintimes = begintime.split('-')
        endtimes = endtime.split('-')

        # print 'begin===>' + str(begintime) + 'end===>' + str(endtime)
        resulttimes = generateNewsUrlMills([begintime, endtime])
        # print str(moviename) + '===>' + 'begintime: ' + str(resulttimes['begin']) + 'endtime: ' + str(resulttimes['end'])
        url = 'http://news.baidu.com/ns?from=news&cl=2&bt='+str(resulttimes['begin'])+'&y0='+str(begintimes[0])+'&m0='+str(begintimes[1])+'&d0='+str(begintimes[2])+'&y1='+str(endtimes[0])+'&m1='+str(endtimes[1])+'&d1='+str(endtimes[2])+'&et='+str(resulttimes['end'])+'&q1='+str(moviename)+'&submit=百度一下&q3=&q4=&mt=0&lm=&s=2&begin_date='+str(begintime)+'&end_date='+str(endtime)+'&tn=newstitledy&ct=0&rn=20&q6='
        try:
            movienewsnum = simpleParseNews(url)
            movieNewsMap[moviename] = movienewsnum
            print str(moviename) + ' news===> ' + str(movieNewsMap[moviename])
        except:
            print str(moviename) + '--- has some problem' + 'with url' + url
            movieNewsMap[moviename] = ''
            proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)

        sleep(3)



    file = open(str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalnews.txt', 'a')
    for key, value in movieNewsMap.items():
        try:
            print 'write to file' + str(key) + '===>' + str(value)
            file.write(str(key) + '-' + str(value) + '\n')
        except:
            print str(key) + '--- has some write problem'
    file.close()

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # parseStarring()
    file = open(str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalnews.txt', 'r')
    data = file.readlines()
    file.close()
    print len(data)
    # parseNews()
