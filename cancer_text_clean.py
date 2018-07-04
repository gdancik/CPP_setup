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
import nltk.stem.porter

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

    writeToFile(inputDirectory, groupType, wordDict)
    
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

    
#    #this method tests both words in each bigram, both words are tested in same loop for stopwords
#    #if the second word is invalid, skip all testing of the following bigram.  Altogether skipping
#    #testing of an individual bigram requires that both words be tested after the skip
#    skip = False #skip iterations of loop if next iteration is known to be invalid
#    bigram = list(nltk.bigrams(words)) #break list of words into bigrams
#    stop_words = stopwords.words('english') #load english stopwords
#    clean = [] #empty list
#
#    
#    for b in bigram: #loop through bigrams
#        valid = True
#        
#        if skip == True: #if skip flagged, reset skip to false and continue to next iteration
#            skip = False
#            continue    
#        
#        #if b[1] is not alphanumeric, is a number, or less than or equal to 2 characters
#        if not b[1].isalnum() or b[1].isdigit() or len(b[1]) <= 2:
#            skip = True #flag skip
#            continue #break to next iteration
#        #if b[0] is not alphanumeric, is a number, or less than or equal to 2 characters
#        if not b[0].isalnum() or b[0].isdigit() or len(b[0]) <= 2:            
#            continue #break to next iteration
#                
#        for w in stop_words: #loop through stop words
#            if w == b[1]: #if second word is a stop word flag invalid and skip, break loop
#                skip = True
#                valid = False
#                break
#            elif w == b[0]: #if first word is a stop word flag invalid and break loop
#                valid = False
#                break
#        if valid == True: #if valid append to clean list
#            clean.append(b)
    

    #This method will test every bigram, regardless of whether or now we know if not valid
    #only need to test b[1] with the exception of the first iteration, flag for the
    #next bigram being valid based off the previous b[1]
    firstBigram = True #if first bigram need to test b[0], flag true
    firstValid = True #bool for validity of b[0]
    nextValid = True #method to check if next bigram is valid, flagged from previous b[1]
    bigram = list(nltk.bigrams(words)) #break list of words into bigrams
    stop_words = stopwords.words('english') #load english stopwords
    clean = [] #empty list
    
    for b in bigram: #loop through bigrams
        
        valid = True #reset/initialize valid as True
        
        if firstBigram == True: #if first bigram
            firstBigram = False #set to false
            #if alphanumeric, not a number, and longer than 2 characters
            if b[0].isalnum() and not b[0].isdigit() and len(b[0]) > 2:
                for w in stop_words: #loop through stop_words
                    if w == b[0]: #if matched in list of stopwords
                        firstValid = False #firstValid is False
                        break #exit for loop
            else: #invalid word length or outside word parameters
                firstValid = False #first word in first bigram is invalid
                
        #if second word of bigram is alphanumeric, not a number, and longer than 2 characters
        if b[1].isalnum() and not b[1].isdigit() and len(b[1]) > 2:
            for w in stop_words:
                if w == b[1]: #if b[1] is a stopword
                    valid = False #set valid to false
                    break #exit for loop
        else:
            valid = False
            
        #if b[0] in first bigram, b[1], and b[1] from the previous bigram are all valid
        if valid == True and nextValid == True and firstValid == True:
            clean.append(b) #add bigram to list
        elif firstValid == False: #if firstValid is set to false
            firstValid = True #set firstValid to true permanently
        
        if valid == False: #if valid is flagged to false, the next bigram is not valid
            nextValid = False
        else: #if valid is flagged to true, the next bigram can also be valid
            nextValid = True
        
    clean = set(clean) #remove duplicates
    
    return addToDict(clean, wordDict) #return updated dictionary


def writeToFile(outputDirectory, groupType, wordDict):
    
    threshold = 10 #threshold for minimum count of word/bigram appearance
    
    #output file into same directory as csv file, Unicode changed back to ascii
    if groupType == "single":
        outFile = inputDirectory + "/cancer_words.csv"
        writeFile = open(outFile, 'w')
        print("Writing file...")
        for word in wordDict: #loop through dictionary
            if wordDict[word] >= threshold:
                writeFile.write(ascii(word) + ',' + str(wordDict[word]) + '\n')
        writeFile.close()            
    
    elif groupType == "bigram": #did elif in case we want to add additional groupings
        outFile = inputDirectory + "/cancer_bigrams.csv"
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
t2 = timeit.default_timer()
commonWords(inputDirectory, groupType, portion)
t3 = timeit.default_timer()
print(t3 - t2)