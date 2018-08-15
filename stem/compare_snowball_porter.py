# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 13:51:24 2018

@author: kewilliams
"""

snowballFile = r"C:/users/kewil/test/cancer_txt/snowball_stem_words.csv"
porterFile = r"C:/users/kewil/test/cancer_txt/porter_stem_words.csv"

sList = []
pList = []

snow = open(snowballFile)
port = open(porterFile)
for line in snow:
    sdata = line.split(',')
    sList.append([sdata[0], sdata[1].strip('\n')])
snow.close()

for line in port:
    pdata = line.split(',')
    pList.append([pdata[0], pdata[1].strip('\n')])
port.close()

sList.sort()
pList.sort()
compList = []

pIndex = 0
sIndex = 0
for i in range(len(pList)):
    if sList[sIndex][0] == pList[pIndex][0]:
        compList.append([sList[sIndex][0], sList[sIndex][1], pList[pIndex][1]])
        pIndex += 1
        sIndex += 1
    elif sList[sIndex][0] < pList[pIndex][0]:
        compList.append([sList[sIndex][0], sList[sIndex][1], '-'])
        sIndex += 1
    elif sList[sIndex][0] > pList[pIndex][0]:
        compList.append([pList[pIndex][0], '-', pList[pIndex][1]])
        pIndex += 1

print(compList)

outFile = r"C:/users/kewil/test/cancer_txt/stemmer_comparison.csv"

writeFile = open(outFile, 'w')
writeFile.write("Stem,SnowballStemmer,PorterStemmer\n")
for item in compList:
    if item[1] != item[2]:
        writeFile.write(item[0] + ',' + item[1] + ',' + item[2] + '\n')
writeFile.close()
