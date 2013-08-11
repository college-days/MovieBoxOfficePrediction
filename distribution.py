#This Python file uses the following encoding: utf-8
# __author__ = 'zjh'

from scipy.stats import f

# print f._ppf(0.95, 2, 9)
# print f._cdf(4.26, 2, 9)
#
# print int('11', 2)
#
# print 1-f._cdf(647.8, 1, 1)

def calcPValue(targetlist, resultlist, paramlist):
    pLength = len(paramlist)
    nLength = len(targetlist)

    print 'pLength--->' + str(pLength)
    print 'nLenght--->' + str(nLength)

    targetAverage = sum(targetlist)/len(targetlist)
    ssr = []
    for item in resultlist:
        ssr.append((item-targetAverage)**2)

    ssrSum = sum(ssr)

    sse = []
    for counter in range(0, nLength):
        sse.append((targetlist[counter]-resultlist[counter])**2)

    sseSum = sum(sse)

    fValue = (ssrSum/pLength)/(sseSum/(nLength-pLength-1))

    pValue = f._cdf(fValue, pLength, nLength-pLength-1)

    return 1-pValue