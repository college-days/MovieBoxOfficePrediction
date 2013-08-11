#This Python file uses the following encoding: utf-8
# __author__ = 'zjh'

from baiduSpider import readExcelFunc
import os

import numpy as np
from sklearn import linear_model
from sklearn.decomposition import PCA
clf = linear_model.LinearRegression()
from distribution import calcPValue
from numpy import array
from numpy import ndarray
from scipy.stats import spearmanr

movieBoxofficeList = []
movieNameList = []
movieWeiboElem = []
movieStarringWeiboElem = []
movieNewsElem = []


def parsedata(datauri, movienamelist):
    resultList = []
    file = open(str(datauri), 'r')
    for line in file.readlines():
        try:
            linesplit = line.split('-')
            moviename = linesplit[0]
            moviedata = linesplit[1]
            # print linesplit
            if moviename in movienamelist:
                resultList.append(int(moviedata))
        except:
            print str(moviename)

    file.close()
    return resultList

def init():
    global movieWeiboElem
    global movieNewsElem
    global movieStarringWeiboElem
    global movieBoxofficeList

    movieBoxofficePath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalboxoffice.txt'
    movieStarringPath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalstarringweibonum.txt'
    movieWeiboPath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalweibo.txt'
    movieNewsPath = str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalnews.txt'

    movieNameList = readExcelFunc()

    movieNewsElem = parsedata(movieNewsPath, movieNameList)
    movieWeiboElem = parsedata(movieWeiboPath, movieNameList)
    movieStarringWeiboElem = parsedata(movieStarringPath, movieNameList)
    movieBoxofficeList = parsedata(movieBoxofficePath, movieNameList)

    # print len(movieNewsElem)
    # print len(movieWeiboElem)
    # print len(movieStarringWeiboElem)
    # print len(movieBoxofficeList)

def calcParams(elemArray, targetArray):
    print 'clea!!!'
    params = []

    clf.fit(np.c_[elemArray], targetArray)

    for item in clf.coef_:
        params.append(item)
    params.append(clf.intercept_)

    print "cleatha!!!"
    print params

    resultArray = params[0]*elemArray + params[1]

    print len(resultArray)

    return [str(clf.score(np.c_[elemArray], targetArray)), str(calcPValue(targetArray, resultArray, [elemArray]))]


def calcBestElem():
    global movieWeiboElem
    global movieNewsElem
    global movieStarringWeiboElem
    global movieBoxofficeList

    init()

    movieBoxofficeArray = array(movieBoxofficeList)
    movieWeiboArray = array(movieWeiboElem)
    movieNewsArray = array(movieNewsElem)
    movieStarringWeiboArray = array(movieStarringWeiboElem)

    weiboResult = calcParams(movieWeiboArray, movieBoxofficeArray)
    print 'weibo R^2 ===> ' + weiboResult[0]
    print 'weibo p-value ===> ' + weiboResult[1]

    starringWeiboResult = calcParams(movieStarringWeiboArray, movieBoxofficeArray)
    print 'starringweibo R^2 ===> ' + starringWeiboResult[0]
    print 'starringweibo p-value ===> ' + starringWeiboResult[1]

    newsResult = calcParams(movieNewsArray, movieBoxofficeArray)
    print 'news R^2 ===> ' + newsResult[0]
    print 'news p-value ===> ' + newsResult[1]

def pca():
    global movieWeiboElem
    global movieNewsElem
    global movieStarringWeiboElem
    global movieBoxofficeList

    init()

    movieBoxofficeArray = array(movieBoxofficeList)
    movieWeiboArray = array(movieWeiboElem)
    movieNewsArray = array(movieNewsElem)
    movieStarringWeiboArray = array(movieStarringWeiboElem)

    print spearmanr(movieWeiboArray, movieBoxofficeArray)
    print spearmanr(movieNewsArray, movieBoxofficeArray)
    print spearmanr(movieStarringWeiboArray, movieBoxofficeArray)

if __name__ == '__main__':
    calcBestElem()
    pca()