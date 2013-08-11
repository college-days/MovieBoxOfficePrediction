#This Python file uses the following encoding: utf-8
# __author__ = 'zjh'

import os
import xlrd

def parseBoxoffice():

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

    # return nameStrList
    # for moviename in nameStrList:
    #     print moviename + '\n'

def filterBoxOffice():
    filesPath = os.path.join(os.path.dirname(__file__), 'Files').replace('\\','/')
    filePath = str(filesPath) + '/boxoffice.xls'
    data = xlrd.open_workbook(str(filePath))
    table = data.sheet_by_index(0)
    nrows = table.nrows

    values = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        values.append(row)

    nameList = [value[0].encode('utf-8') for value in values]
    simpleNameList = list(set(nameList))
    simpleNameList.sort(key=nameList.index)

    for value in values:
        print value[0].encode('utf-8')

    for name in simpleNameList:
        print name

    movieDict = {}
    for name in simpleNameList:
        boxofficeList = []
        for value in values:
            if value[0].encode('utf-8') == name:
                print '---------------------'
                boxofficeList.append(value[3])

        print boxofficeList
        maxboxoffice = max([int(boxoffice) for boxoffice in boxofficeList])
        movieDict[name] = maxboxoffice

    for key, value in movieDict.items():
        print str(key) + "--->" + str(value) + "\n"

    file = open(str(os.path.join(os.path.dirname(__file__), 'Files').replace('\\', '/')) + '/movietotalboxoffice.txt', 'a')
    for key, value in movieDict.items():
        file.write(str(key) + '-' + str(value) + '\n')
    file.close()

    print 'movietotal' + str(len(movieDict))

if __name__ == '__main__':
    # parseBoxoffice()
    filterBoxOffice()