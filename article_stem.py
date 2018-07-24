# -*- coding: utf-8 -*-
"""
Usage:

  article_stem.py [-h] inputFile outputFile fileType(single/bigram)

Code to stem words from csv files containing words and bigrams.  To a new csv file,
the code writes the stem word/bigrams and a list of the words/bigrams that created them

"""

from pathlib import Path
import argparse
import sys
from nltk.stem import PorterStemmer

def testArgs(inputFile, fileType):
    
    valid = True   
    if fileType != "single" and fileType != "bigram": #check valid filetype
        print("invalid word grouping")
        valid = False   
    if not Path(inputFile).is_file(): #check valid filepath for input
        print("file not found")
        valid = False   
    if valid == False: #if invalid exit code
        exit()
    

def wordStem(inputFile):
    
    stemmer = PorterStemmer()
    
    stemList = []
    stemTable = []
    
    for line in open(inputFile): #iterate through input file
        temp = line.strip().split(',') #temp[0] has word, temp[1] has count
        word = stemmer.stem(eval(temp[0]))
        
        if word not in stemList:
            stemTable.append([word, temp[0]]) #add stem and word that created it
            stemList.append(word) #add stem to list
        else: #if stem already present
            nonstemmed = stemTable[stemList.index(word)][1] #string of words that created stem
            #overwrite index to have stem and add new word that created the stem to the string
            stemTable[stemList.index(word)] = [word, nonstemmed + ' - ' + temp[0]] 
    #print(stemTable)
    return stemTable


def bigramStem(inputFile):
    
    stemmer = PorterStemmer()
    
    stemTable = []
    wordList1 = []
    wordList2 = []
        
    for line in open(inputFile):

        index = -1
        
        temp = line.strip().split(',') #temp[0] word 1, temp[1] word 2, temp[2] count
        word1 = stemmer.stem(eval(temp[0])) #eval word1 before stem
        word2 = stemmer.stem(eval(temp[1])) #eval word2 before stem
        
        #if both words in their respective word lists
        #nested if to reduce searches if first word not found
        if word1 in wordList1:
            if word2 in wordList2:
                #index of bigram if found, otherwise -1
                index = findMatch(word1, wordList1, word2, wordList2)

        if index == -1: #if bigram not found, append words to list
            wordList1.append(word1)
            wordList2.append(word2)
            #append words and full words that created the stems
            stemTable.append([word1, word2, temp[0] + ' ' + temp[1]])

        else: #if bigram in list
            nonstemmed = stemTable[index][2] #string of words that produce the stem
            #overwrite entry to have stem, string of old words concatenated with the new one
            stemTable[index] = [word1, word2, nonstemmed + ' - ' + temp[0] + ' ' + temp[1]]

    #print(stemTable)
    return stemTable


def findMatch(word1, wordList1, word2, wordList2):
        
    #list of indices for each occurance of the word in their respective lists
    indexWordList1 = [i for i, w in enumerate(wordList1) if w == word1]
    indexWordList2 = [i for i, w in enumerate(wordList2) if w == word2]
    
    #search for matching index indicating stemmed bigram already present    
    index = list(set(indexWordList1).intersection(indexWordList2))

    if not index: #if no match
        return -1
    else:
        return index[0] #return the index of the match
           

#def bigramStemOld(inputFile):
#    
#    stemTable = []
#    stemList = []
#    stemList.append([0,0])
#    stemmer = PorterStemmer()
#    
#    for line in open(inputFile):
#
#        temp = line.strip().split(',') #temp[0] word 1, temp[1] word 2, temp[2] count
#        word1 = stemmer.stem(eval(temp[0])) #eval word1 before stem
#        word2 = stemmer.stem(eval(temp[1])) #eval word2 before stem
#        
#        indexList = []
#        firstMatch = False
#        fullMatch = False
#        
#        for i in range(len(stemList)): #iterate through list
#            if word1 == stemList[i][0]: #if match, track index of match and flag match
#                indexList.append(i)
#                firstMatch = True
#        
#        if firstMatch == True: #if first match
#            for index in indexList: #iterate through matched indices
#                if stemList[index][1] == word2: #if both words found, flag match and exit
#                    fullMatch = True
#                    break
#        
#        if fullMatch != True: #if full word not in stemList, append to words to stemList
#            stemList.append([word1, word2])
#            #append words and full words that created the stems
#            stemTable.append([word1, word2, temp[0] + ' ' + temp[1]])
#        else: #if full word in list
#            nonstemmed = stemTable[index - 1][2] #string of words that produce the stem
#            #overwrite entry to have stem, string of old words concatenated with the new one
#            stemTable[index - 1] = [word1, word2, nonstemmed + ' - ' + temp[0] + ' ' + temp[1]]
#        
#    #print(stemTable)
#    return stemTable


def writeToFile(stemTable, outFile, fileType):
    writeFile = open(outFile, 'w')
    if fileType == "single":
        for i in range(len(stemTable)): 
            #stemTable[0] has stem, stemTable[1] has words that produced the stem
            writeFile.write(ascii(stemTable[i][0]) + ',' + stemTable[i][1] + '\n')
    elif fileType == "bigram":
        for i in range(len(stemTable)):
            #stemTable[0] has stem 1, stemTable[1] has stem 2, 
            #stemTable[2] has list of words that produce stem 
            writeFile.write(ascii(stemTable[i][0]) + ',' + ascii(stemTable[i][1]) + ',' + 
                            stemTable[i][2] + '\n')
            
    
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


testArgs(inputFile, fileType) #test for valid argumends from command line

print("Executing Code...")
if fileType == "single":
    stemTable = wordStem(inputFile)
elif fileType == "bigram":
    stemTable = bigramStem(inputFile)

writeToFile(stemTable, outFile, fileType)
    

#wordStem(r"C:/users/kewil/test/cancer_txt/cancer_words.csv")
#bigramStem(r"C:/users/kewil/test/cancer_txt/cancer_bigrams.csv")
#bigramStemOld(r"C:/users/kewil/test/cancer_txt/cancer_bigrams.csv")