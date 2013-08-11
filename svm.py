#This Python file uses the following encoding: utf-8
# __author__ = 'zjh'

from leastsquarePre import readExcelFunc
import os
from sklearn import svm

movieBoxofficeSvmList = []
movieWeiboSvmList = []
movieNewsSvmList = []
movieStarringSvmList = []
finalDataList = []

def parseBoxofficeFile(path):
    boxofficeList = []

    file = open(path, 'r')
    for line in file.readlines():
        data = line.split('-')
        boxofficeList.append(int(data[1]))
    file.close()

    middleboxoffice = (max(boxofficeList) - min(boxofficeList))/33 + min(boxofficeList)
    # svmResultList = [lambda :x >middleboxoffice ? 1 : -1 for data in boxofficeList]
    svmResult = []
    for data in boxofficeList:
        if int(data) >= middleboxoffice:
            print 'cleantha'
            svmResult.append(1)
        else:
            svmResult.append(-1)

    print len([x for x in svmResult if x == 1])

    return svmResult

def parseDataFile(path):
    dataList = []

    file = open(path, 'r')
    for line in file.readlines():
        data = line.split('-')
        dataList.append(int(data[1]))
    file.close()

    return dataList

def init():
    global movieBoxofficeSvmList
    global movieWeiboSvmList
    global movieNewsSvmList
    global movieStarringSvmList
    global finalDataList

    movieBoxofficePath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalboxoffice.txt'
    movieStarringPath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalstarringweibonum.txt'
    movieWeiboPath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalweibo.txt'
    movieNewsPath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalnews.txt'

    movieBoxofficeSvmList = parseBoxofficeFile(movieBoxofficePath)
    movieWeiboSvmList = parseDataFile(movieWeiboPath)
    movieNewsSvmList = parseDataFile(movieNewsPath)
    movieStarringSvmList = parseDataFile(movieStarringPath)

    print len(movieBoxofficeSvmList)
    print len(movieWeiboSvmList)
    print len(movieNewsSvmList)
    print len(movieStarringSvmList)

    print movieBoxofficeSvmList

    for i in range(0, len(movieBoxofficeSvmList)):
        finalDataList.append([movieWeiboSvmList[i], movieNewsSvmList[i], movieStarringSvmList[i]])

    print len(finalDataList)
    print finalDataList

def svmFunc():
    init()

    global finalDataList
    global movieBoxofficeSvmList

    X = [[0, 0, 0], [2, 2, 1], [3, 3, 3]]
    y = [-1, 1, 1]
    clf = svm.SVR()
    print clf.fit(finalDataList, movieBoxofficeSvmList)
    print clf.fit(X, y)


if __name__ == '__main__':
    # init()
    svmFunc()
