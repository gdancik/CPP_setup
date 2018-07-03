# -*- coding: utf-8 -*-
"""
Usage:

  cancer_text_clean.py [-h] inputDirectory groupType(single/bigram) portion(title/abstract)

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

def testValid (groupType, portion):
    
    valid = True
    
    if portion != "abstract" and portion != "title":
        print("Invalid segment of text files")         
        valid = False
    if groupType != "single" and groupType != "bigram":
        print("Invalid grouping of words")
        valid = False
    
    if valid == False:
        exit()

def commonWords (inputDirectory, groupType, portion):
    
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
            
            #once portion of text is broken into a list without punctuation and ', ", - to null
            #regardless of type of grouping, updated dictionary returned after previous passed with
            #partially clean list of words
            if groupType == "single":
                wordDict = singleWords(words, wordDict)
            else:
                wordDict = bigrams(words, wordDict)
    
        t1 = timeit.default_timer()
        print("Processing complete : " + os.path.basename(inFile) + " : " + str(t1 - t0))

    #output file into same directory as csv file, Unicode changed back to ascii
    if groupType == "single":
        outFile = inputDirectory + "/cancer_words.csv"
        writeFile = open(outFile, 'w')
        print("Writing file...")
        for word in wordDict: #loop through dictionary
            writeFile.write(ascii(word) + ',' + str(wordDict[word]) + '\n')
        writeFile.close()            
    elif groupType == "bigram":
        outFile = inputDirectory + "/cancer_bigrams.csv"
        writeFile = open(outFile, 'w')
        print("Writing file...")     
        for word in wordDict: #loop through dictionary
            #print individual words to unique columns
            writeFile.write(ascii(word[0]) + ',' + ascii(word[1]) + ',' + str(wordDict[word]) + '\n')
            #both words in same column separated by a space
#            writeFile.write(ascii(word[0]) + ' ' + ascii(word[1]) + ',' + str(wordDict[word]) + '\n')
        writeFile.close()
    
def addToDict (clean, wordDict):
    
    #iterate through list
    for word in clean:
        if word not in wordDict: #if not in dict, add as key with value 1
            wordDict[word] = 1
        else:                   #if already in dict, increase value (count) by 1
            wordDict[word] += 1
    
    return wordDict

def singleWords (words, wordDict):
    
    #modify list for alphanumeric words and remove words that only consist of numbers 
    words = [w for w in words if w.isalnum() and not w.isdigit() and len(w) > 2]
    
    #load english stop words and remove them from the list of words
    stop_words = stopwords.words('english')
    clean = [w for w in words if not w in stop_words]
    
    clean = set(clean) #remove duplicates
    
    return addToDict(clean, wordDict) #return updated dictionary
    

def bigrams (words, wordDict):

    skip = False #skip iterations of loop if next iteration is known to be invalid
    bigram = list(nltk.bigrams(words)) #break list of words into bigrams
    stop_words = stopwords.words('english') #load english stopwords
    clean = [] #empty list

    for b in bigram: #loop through bigrams
        
        if skip == True: #if skip flagged, return skip to false and continue to next iteration
            skip = False
            continue    
        
        #if b[0] is alphanumeric, not a number, and long than 2 characters
        if b[0].isalnum() and not b[0].isdigit() and len(b[0]) > 2:
            #if b[1] is not alphanumeric, is a number, and less than or equal to 2 characters
            if not b[1].isalnum() or b[1].isdigit() or len(b[1]) <= 2:            
                skip = True #flag skip
                continue #break to next iteration
            else:
                valid = True #flag valid
                for w in stop_words: #loop through stop words
                    if w == b[0]: #if first word is a stop word flag invalid
                        valid = False
                        break
                    elif w == b[1]: #if second word is stop word flag invalid and skip
                        skip = True
                        valid = False
                        break
                if valid == True: #if valid append to clean list
                    clean.append(b)
    
    clean = set(clean) #remove duplicates
    
    return addToDict(clean, wordDict) #return updated dictionary

# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Clean and retrieve words/bigrams from cancer text files')
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("groupType", help = "type of word grouping (single or bigram)")
ap.add_argument("portion", help = "portion of files (title or abstract)")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

inputDirectory = args['inputDirectory']
groupType = args['groupType']
portion = args['portion']            

groupType = groupType.lower()
portion = portion.lower()
testValid(groupType, portion)

commonWords(inputDirectory, groupType, portion)