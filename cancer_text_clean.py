# -*- coding: utf-8 -*-
"""
Usage:

  cancer_text_clean.py [-h] inputDirectory

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
import glob
import argparse
import sys
import os
import timeit

def cleanText (inputDirectory):

    wordDict = {} #empty dictionary of words in text
    
    #characters to be replaced with a null string " ' -
    #create pattern for regex single pass replacement in string
    rep = {'\'': '', '\"': '', '-': ''}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    
    files = sorted(glob.glob(inputDirectory + "/*.txt"))
    for inFile in files:
        t0 = timeit.default_timer()
        cancerFile = open(inFile, 'r')
        for line in cancerFile:
            
            #split line into its tab deliminated parts
            article = line.split('\t')
            text = eval(article[1].lower()) #portion of article, preserve unicode
        
            #perform regex to alter specified characters
            text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
            
            #list of words in title
            words = text.split()
            
            #remove punctuation
            table = str.maketrans('', '', string.punctuation)
            words = [w.translate(table) for w in words]
            
            #modify list for alphanumeric words and remove words that only consist of numbers 
            words = [w for w in words if w.isalnum() and not w.isdigit()]
            
            #load english stop words and remove them from the list of words
            stop_words = stopwords.words('english')
            clean = [w for w in words if not w in stop_words]
            
            set(clean) #remove duplicates
            for word in clean:
                if word not in wordDict: #if not in dict, add as key with value 1
                    wordDict[word] = 1
                else:                   #if already in dict, increase value (count) by 1
                    wordDict[word] += 1
        t1 = timeit.default_timer()
        print("Processing complete : " + os.path.basename(inFile) + " : " + str(t1 - t0))
    
    #output file into same directory as csv file, Unicode changed back to ascii
    outFile = inputDirectory + "/cancer_words.csv"
    writeFile = open(outFile, 'w')
    print("Writing file...")
    for word in wordDict: #loop through dictionary
        writeFile.write(ascii(word) + ',' + str(wordDict[word]) + '\n')
    writeFile.close()
    
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Clean and retrieve words from cancer text files')
ap.add_argument("inputDirectory", help = "directory of input files")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

inputDirectory = args['inputDirectory']

cleanText(inputDirectory)