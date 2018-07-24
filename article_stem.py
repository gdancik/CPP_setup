# -*- coding: utf-8 -*-
"""
Usage:

  article_stem.py [-h] inputFile fileType(single/bigram)

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
    stemTable = [[]]
    
    for line in open(inputFile):
        temp = line.strip().split(',')
        word = stemmer.stem(eval(temp[0]))
        if word not in stemList:
            stemTable.append([word, temp[1], temp[0]])
            stemList.append(word)
        else:
            loc = stemList.index(word)
            count = stemTable[loc + 1][1]
            nonstemmed = stemTable[loc + 1][2]
            stemTable[loc + 1] = [word, int(count) + int(temp[1]), nonstemmed + ', ' + temp[0]]
    print(stemTable)

#def bigramStem(inputFile):
#    
#    stemmer = PorterStemmer()
#    
#    stemList = []
#    stemTable = [[]]
#        
#    for line in open(inputFile):
    
## main program
## construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser(description='Clean and retrieve words/bigrams from cancer text files')
#ap.add_argument("inputFile", help = "file to be run")
#ap.add_argument("fileType", help = "word grouping in text file (single or bigram)")
#
## print help if no arguments are provided
#if len(sys.argv)==1:
#    ap.print_help(sys.stderr)
#    sys.exit(1)
#
#args = vars(ap.parse_args())
#
#inputFile = args['inputFile']
#fileType = args['fileType'].lower()
#
#testArgs(inputFile, fileType)
#
#if fileType == "single":
#    wordStem(inputFile)
#elif fileType == "bigram":
#    bigramStem(inputFile)
wordStem(r"C:/users/kewil/test/cancer_txt/cancer_words.csv")
