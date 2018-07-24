# -*- coding: utf-8 -*-
"""
Usage:

  article_stem.py [-h] inputFile outputFile fileType(single/bigram)

Code to clean and retrieve words from cancer related text files
Code runs from command line and reads all text files in the directory 
and returns a csv file into the same directory

"""

from pathlib import Path
import argparse
import sys
from nltk.stem import PorterStemmer

def testArgs(inputFile, fileType):
    
    valid = True   
    if fileType != "single" and fileType != "bigram":
        print("invalid word grouping")
        valid = False   
    if not Path(inputFile).is_file():
        print("file not found")
        valid = False   
    if valid == False:
        exit()
    

def wordStem(inputFile):
    
    stemmer = PorterStemmer()
    
    stemList = []
    stemTable = []
    
    for line in open(inputFile):
        temp = line.strip().split(',')
        word = stemmer.stem(eval(temp[0]))
        
        if word not in stemList:      
            stemTable.append([word, temp[1], temp[0]])
            stemList.append(word)
        else:
            loc = stemList.index(word) #this seems to pull the index prior to the desired word
            count = stemTable[loc][1]
            nonstemmed = stemTable[loc][2]
            stemTable[loc] = [word, int(count) + int(temp[1]), nonstemmed + ' - ' + temp[0]]
    
    return stemTable


def bigramStem(inputFile):
    
    stemmer = PorterStemmer()
    
    stemList = []
    stemList.append([0,0])
    stemTable = []
        
    for line in open(inputFile):

        temp = line.strip().split(',')
        word1 = stemmer.stem(eval(temp[0]))
        word2 = stemmer.stem(eval(temp[1]))
        
        firstMatch = False
        fullMatch = False
        
        indexList = []
        for i in range(len(stemList)):
            if word1 == stemList[i][0]:
                indexList.append(i)
                firstMatch = True
        
        if firstMatch == True:
            for index in indexList:
                if stemList[index][1] == word2:
                    fullMatch = True
                    break
        
        if fullMatch != True:
            stemList.append([word1, word2])
            stemTable.append([word1, word2, temp[2], eval(temp[0]) + ' ' + eval(temp[1])])
        else:
            count = stemTable[index - 1][2]
            nonstemmed = stemTable[index - 1][3]
            stemTable[index - 1] = [word1, word2, int(count) + int(temp[2]),
                     nonstemmed + ' - ' + eval(temp[0]) + ' ' + eval(temp[1])]
    return stemTable


def writeToFile(stemTable, outFile, fileType):
    writeFile = open(outFile, 'w')
    if fileType == "single":
        for i in range(len(stemTable)):
            writeFile.write(ascii(stemTable[i][0]) + ',' + str(stemTable[i][1]) + ',' + 
                            ascii(stemTable[i][2]) + '\n')
    elif fileType == "bigram":
        for i in range(len(stemTable)):
            writeFile.write(ascii(stemTable[i][0]) + ',' + ascii(stemTable[i][1]) + ',' + 
                            str(stemTable[i][2]) + ',' + ascii(stemTable[i][3]) + '\n')
            
    
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Clean and retrieve words/bigrams from cancer text files')
ap.add_argument("inputFile", help = "file to be run")
ap.add_argument("outFile", help = "output file path and name")
ap.add_argument("fileType", help = "word grouping in text file (single or bigram)")


# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

inputFile = args['inputFile']
outFile = args['outFile']
fileType = args['fileType'].lower()


testArgs(inputFile, fileType)

if fileType == "single":
    stemTable = wordStem(inputFile)
elif fileType == "bigram":
    stemTable = bigramStem(inputFile)

writeToFile(stemTable, outFile, fileType)
    

#wordStem(r"C:/users/kewil/test/cancer_txt/cancer_words.csv")
#bigramStem(r"C:/users/kewil/test/cancer_txt/cancer_bigrams.csv")
