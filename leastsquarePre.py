#This Python file uses the following encoding: utf-8
# __author__ = 'zjh'

import xlrd
import os

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

def parseFile(path):
    resultMap = {}
    file = open(path, 'r')
    for line in file.readlines():
        data = line.split('-')
        resultMap[data[0]] = data[1]
    file.close()

    return resultMap

def combineData():
    movieBoxofficePath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalboxoffice.txt'
    movieStarringPath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalstarringweibonum.txt'
    movieWeiboPath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalweibo.txt'
    movieNewsPath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalnews.txt'

    movieBoxofficeMap = {}
    movieStarringMap = {}
    movieWeiboMap = {}
    movieNewsMap = {}

    movieBoxofficeMap = parseFile(movieBoxofficePath)
    movieStarringMap = parseFile(movieStarringPath)
    movieWeiboMap = parseFile(movieWeiboPath)
    movieNewsMap = parseFile(movieNewsPath)

    finalMovieMap = {}
    movieNameList = readExcelFunc()
    for moviename in movieNameList:
        movieAttris = []
        movieAttris.append(movieBoxofficeMap[moviename])
        movieAttris.append(movieStarringMap[moviename])
        movieAttris.append(movieWeiboMap[moviename])
        movieAttris.append(movieNewsMap[moviename])

        finalMovieMap[moviename] = movieAttris

    for key, value in finalMovieMap.items():
        print str(key) + '===>' + 'boxoffice: ' + str(value[0]) + 'starring: ' + str(value[1]) + 'weibo: ' + str(value[2]) + 'news: ' + str(value[3])

    print len(finalMovieMap)

    return finalMovieMap

if __name__ == '__main__':
  combineData()