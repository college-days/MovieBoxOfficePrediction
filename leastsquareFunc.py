#This Python file uses the following encoding: utf-8
# __author__ = 'zjh'

from leastsquarePre import combineData

import numpy as np
from sklearn import linear_model
clf = linear_model.LinearRegression()
from distribution import calcPValue
from numpy import array

y = []
x1 = []
x2 = []
x3 = []

# yArray = array()
# x1Array = array()
# x2Array = array()
# x3Array = array()

#y-boxoffice x1-starringweibo x2-movieweibo x3 movienews
def initXY():
    movieAttriMap = combineData()

    for key, value in movieAttriMap.items():
        print str(key) + '===>' + 'boxoffice: ' + str(value[0]) + 'starring: ' + str(value[1]) + 'weibo: ' + str(value[2]) + 'news: ' + str(value[3])
        y.append(int(value[0]))
        x1.append(int(value[1]))
        x2.append(int(value[2]))
        x3.append(int(value[3]))

    print len(movieAttriMap)

def calcRSquare(targetlist, resultlist):
    if cmp(len(targetlist), len(resultlist)) == 0:
        length = len(targetlist)
        u = []
        for rcounter in range(0, length):
            u.append((targetlist[rcounter] - resultlist[rcounter])**2)

        usum = sum(u)

        average = sum(targetlist)/len(targetlist)
        v = []
        for rcounter in range(0, length):
            print np.int64((targetlist[rcounter] - average)**2)
            v.append(long((targetlist[rcounter] - average)**2))

        vsum = sum(v)

        return 1-(usum/vsum)

def leastsq():
    initXY()

    ymax = max(y)
    ymin = min(y)
    ymm = ymax-ymin
    x1max = max(x1)
    x1min = min(x1)
    x1mm = x1max-x1min
    x2max = max(x2)
    x2min = min(x2)
    x2mm = x2max-x2min
    x3max = max(x3)
    x3min = min(x3)
    x3mm = x3max-x3min

    mms = [ymm, x1mm, x2mm, x3mm]

    print mms

    maxmm = max(mms)

    print maxmm

    x1Array = array(x1)
    x2Array = array(x2)
    x3Array = array(x3)
    yArray = array(y)

    # print yArray
    # print maxmm/ymm

    x1Array *= maxmm/x1mm
    x2Array *= maxmm/x2mm
    x3Array *= maxmm/x3mm
    yArray *= maxmm/ymm

    print max(yArray)-min(yArray)
    print max(x1Array)-min(x1Array)
    print max(x2Array)-min(x2Array)
    print max(x3Array)-min(x3Array)
    # print yArray
    clf.fit(np.c_[x1Array, x2Array, x3Array], yArray)
    print clf.coef_, clf.intercept_

    params = []

    for item in clf.coef_:
        # print item
        params.append(item)

    params.append(clf.intercept_)

    yRegression = params[0]*x1Array + params[1]*x2Array + params[2]*x3Array + params[3]

    for i in range(0, len(yArray)):
        print str(yArray[i]) + '===' + str(yRegression[i])


    print 'R^2--->' + str(clf.score(np.c_[x1Array, x2Array, x3Array], yArray))

    print 'p-value--->' + str(calcPValue(yArray, yRegression, [x1Array, x2Array, x3Array]))

    #if not divide ymm it will overflow and become negative= =
    yArray /= ymm
    yRegression /= ymm
    print 'Rsquare--->' + str(calcRSquare(yArray, yRegression))


if __name__ == '__main__':
    # initXY()
    leastsq()