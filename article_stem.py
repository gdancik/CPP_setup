# -*- coding: utf-8 -*-
"""
Usage:

  article_stem.py [-h] inputFile outputFile fileType(word/bigram)

Code to stem words from csv files containing words and bigrams.  To a new csv file,
the code writes the stem word/bigrams and a list of the words/bigrams that created them

"""

from pathlib import Path
import argparse
import sys
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

def testArgs(inputFile, fileType):
    
    valid = True   
    if fileType != "word" and fileType != "bigram": #check valid filetype
        print("invalid word grouping")
        valid = False   
    if not Path(inputFile).is_file(): #check valid filepath for input
        print("file not found")
        valid = False   
    if valid == False: #if invalid exit code
        exit()
    

def wordStem(inputFile):
    
    #stemmer = PorterStemmer()
    stemmer = SnowballStemmer("english")
    
    stemList = []
    stemTable = []
    
    for line in open(inputFile): #iterate through input file
        temp = line.strip().split(',') #temp[0] has word, temp[1] has count
        word = stemmer.stem(eval(temp[0]))
        
        if word not in stemList:
            stemTable.append([word, temp[1], eval(temp[0])]) #add stem, count, and word
            stemList.append(word) #add stem to list
        else: #if stem already present
            nonstemmed = stemTable[stemList.index(word)][2] #string of words that created stem
            count = stemTable[stemList.index(word)][1]
            #overwrite index to have stem, increase count, and add new word to the string
            stemTable[stemList.index(word)] = [word, int(count) + int(temp[1]), 
                      nonstemmed + ' - ' + eval(temp[0])] 
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
            #append words, count and full words that created the stems
            stemTable.append([word1, word2, temp[2], eval(temp[0]) + ' ' + eval(temp[1])])

        else: #if bigram in list
            nonstemmed = stemTable[index][3] #string of words that produce the stem
            count = stemTable[index][2]
            #overwrite entry to have stem, string of old words concatenated with the new one
            stemTable[index] = [word1, word2, int(count) + int(temp[2]),
                     nonstemmed + ' - ' + eval(temp[0]) + ' ' + eval(temp[1])]

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


def writeToFile(stemTable, outFile, fileType):
    writeFile = open(outFile, 'w')
    if fileType == "word":
        for i in range(len(stemTable)): 
            #stemTable[0] has stem, stemTable[1] has words that produced the stem
            writeFile.write(ascii(stemTable[i][0]) + ',' + str(stemTable[i][1]) + ',' +
                            ascii(stemTable[i][2]) + '\n')
    elif fileType == "bigram":
        for i in range(len(stemTable)):
            #stemTable[0] has stem 1, stemTable[1] has stem 2, 
            #stemTable[2] has list of words that produce stem 
            writeFile.write(ascii(stemTable[i][0]) + ',' + ascii(stemTable[i][1]) + ',' + 
                            str(stemTable[i][2]) + ',' + ascii(stemTable[i][3]) + '\n')
            
    
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Stem words/bigrams in .csv files and write to new updated file')
ap.add_argument("inputFile", help = "file to be run")
ap.add_argument("outFile", help = "output file path and name")
ap.add_argument("fileType", help = "word grouping in text file (word or bigram)")


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
if fileType == "word":
    stemTable = wordStem(inputFile)
elif fileType == "bigram":
    stemTable = bigramStem(inputFile)

writeToFile(stemTable, outFile, fileType)
    

#wordStem(r"C:/users/kewil/test/cancer_txt/cancer_words.csv")
#bigramStem(r"C:/users/kewil/test/cancer_txt/cancer_bigrams.csv")
#bigramStemOld(r"C:/users/kewil/test/cancer_txt/cancer_bigrams.csv")