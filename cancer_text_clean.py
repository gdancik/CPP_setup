# -*- coding: utf-8 -*-
"""
Usage:

  cancer_text_clean.py [-h] inputDirectory outputFile[with filepath] groupType(word/bigram) portion(title/abstract)

Code to clean and retrieve words from cancer related text files
Code runs from command line and reads all text files in the directory 
and returns a csv file into the same directory

After text file is read in, line.split() seperates into 6 parts
[0] - pmid
[1] - title
[2] - author
[3] - journal
[4] - year
[5] - abstract
Can adjust "text = article[x].lower()" to reflect desired data to be read
"""

import re
import string
from nltk.corpus import stopwords
import nltk
import glob
import argparse
import sys
import os
import timeit
import nltk.stem.porter

def testValidArguments (groupType, portion):
    
    valid = True
    
    if portion != "abstract" and portion != "title":
        print("Invalid segment of text files")         
        valid = False
    if groupType != "word" and groupType != "bigram":
        print("Invalid grouping of words")
        valid = False
    
    if valid == False:
        exit()

def commonWords (inputDirectory, outFile, groupType, portion):
    
    wordDict = {} #empty dictionary of words in text

    #characters to be replaced with a null string: \" OR \' OR \-
    #create pattern for regex single pass replacement in string
    pattern = re.compile("\'|\"|\-")
    
    files = sorted(glob.glob(inputDirectory + "/*.txt"))
    print("Number of *.txt files found in directory '", inputDirectory, "': ", len(files), sep = "")

    if portion == "abstract": #if abstract, index 5 in list
        portion = 5
    else:
        portion = 1 #if title, index 1 in list

    for inFile in files:
        t0 = timeit.default_timer()
        cancerFile = open(inFile, 'r')
        for line in cancerFile:
            
            article = line.split('\t')
            text = eval(article[portion].lower())
            text = pattern.sub('', text)
            
            words = text.split()
            #remove punctuation
            table = str.maketrans('', '', string.punctuation)
            words = [w.translate(table) for w in words]
            stop_words = stopwords.words('english') #load english stopwords
            
            #once portion of text is broken into a list without punctuation and ', ", - to null
            #regardless of type of grouping, updated dictionary returned after previous passed with
            #partially clean list of words
            if groupType == "word":
                wordDict = singleWords(words, wordDict, stop_words)
            else:
                wordDict = bigrams(words, wordDict, stop_words)
    
        t1 = timeit.default_timer()
        print("Processing complete : " + os.path.basename(inFile) + " : " + str(t1 - t0))

    writeToFile(inputDirectory, outFile, groupType, wordDict)
    
def addToDict (clean, wordDict):    
    #iterate through list
    for word in clean:
        if word not in wordDict: #if not in dict, add as key with value 1
            wordDict[word] = 1
        else:                   #if already in dict, increase value (count) by 1
            wordDict[word] += 1
    
    return wordDict

def testValid(word, stop_words):
    valid = True
    if word.isalnum() and not word.isdigit() and len(word) > 2:
        for w in stop_words:
            if w == word:
                valid = False
                break
    else:
        valid = False
    
    return valid

def singleWords (words, wordDict, stop_words):
    
    clean = []
    for word in words:
        valid = testValid(word, stop_words)
        if valid == True:
            clean.append(word)
    
    clean = set(clean) #remove duplicates
    
    return addToDict(clean, wordDict) #return updated dictionary
    
 
def bigrams (words, wordDict, stop_words):

    bigram = list(nltk.bigrams(words)) #break list of words into bigrams

    clean = [] #empty list
    
    for i in range(len(bigram)):
        
        b = bigram[i]    
        
        valid = testValid(b[1], stop_words)
        if not valid:
            i += 2
            continue
        
        valid = testValid(b[0], stop_words)
        if valid:
            clean.append(b)
        i += 1
        
    clean = set(clean) #remove duplicates
    
    return addToDict(clean, wordDict) #return updated dictionary


def writeToFile(outputDirectory, outFile, groupType, wordDict):
    
    #output file into same directory as csv file, Unicode changed back to ascii
    if groupType == "word":
        threshold = 5
        writeFile = open(outFile, 'w')
        print("Writing file...")
        for word in wordDict: #loop through dictionary
            if wordDict[word] >= threshold:
                writeFile.write(ascii(word) + ',' + str(wordDict[word]) + '\n')
        writeFile.close()            
    
    elif groupType == "bigram": #did elif in case we want to add additional groupings
        threshold = 5
        writeFile = open(outFile, 'w')
        print("Writing file...")     
        for word in wordDict: #loop through dictionary
            if wordDict[word] >= threshold:
                #print individual words to unique columns
                writeFile.write(ascii(word[0]) + ',' + ascii(word[1]) + ',' + str(wordDict[word]) + '\n')
                #both words in same column separated by a space
#                writeFile.write(ascii(word[0]) + ' ' + ascii(word[1]) + ',' + str(wordDict[word]) + '\n')
        writeFile.close()

# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Clean and retrieve words/bigrams from cancer text files')
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputFile", help = "output filepath and name")
ap.add_argument("groupType", help = "type of word grouping (single or bigram)")
ap.add_argument("portion", help = "portion of files (title or abstract)")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

inputDirectory = args['inputDirectory']
outFile = args['outputFile']
groupType = args['groupType']
portion = args['portion']            

groupType = groupType.lower()
portion = portion.lower()
testValidArguments(groupType, portion)
t2 = timeit.default_timer()
commonWords(inputDirectory, outFile, groupType, portion)
t3 = timeit.default_timer()
print(t3 - t2)