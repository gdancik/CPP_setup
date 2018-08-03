# -*- coding: utf-8 -*-
"""
Usage:

  pmid_and_stem.py [-h] inputDirectory outputDirectory

Code to alter cancer text files to write pmid and stemmed words
Code runs from command line and reads all text files in the directory 
and returns text files in the designated output directory

After text file is read in, line.split() seperates into 6 parts
[0] - pmid
[1] - title
[2] - author
[3] - journal
[4] - year
[5] - abstract
Can adjust text = article[x] to reflect desired data to be read
"""

import re
import string
from nltk.corpus import stopwords
import glob
import argparse
import sys
import os
import timeit
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

def convertText(inputDirectory, outputDirectory):
    
    #characters to be replaced with a null string: \" OR \' OR \-
    #create pattern for regex single pass replacement in string
    pattern = re.compile("\'|\"|\-")
    
    #stemmer = PorterStemmer()
    stemmer = SnowballStemmer("english")
    
    files = sorted(glob.glob(inputDirectory + "/*.txt"))
    print("Number of *.txt files found in directory '", inputDirectory, "': ", len(files), sep = "")

    # create outputDirectory if it does not exist
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
        
    for inFile in files:
        
        t0 = timeit.default_timer()
        #alter name to reflect article stem
        outFile = outputDirectory + "/stem_" + os.path.basename(inFile) 
        writeFile = open(outFile, 'w')
        cancerFile = open(inFile, 'r')
        for line in cancerFile:
            
            article = line.split('\t')
            text = eval(article[1].lower()) + ' ' + eval(article[5].lower())
            text = pattern.sub('', text)
            
            words = text.split()
            #remove punctuation
            table = str.maketrans('', '', string.punctuation)
            words = [w.translate(table) for w in words]
            stop_words = stopwords.words('english') #load english stopwords
            
            #tried this several ways to see if it mattered for efficiency.  Considering the
            #number of concatenations and the fact that each concatenations creates a new string 
            #object each time, thus using text += word + ' ' seems bad.
            #doing a join at the very end seems to take a little longer but does the smallest
            #amount of memory reallocations for strings
            
            #text = "" #empty string of text
            text = [] #empty list
            
            for word in words: #iterate through list of words
                valid = True #flag true
                
                #if alphanumeric, not a number, and more than 2 characters
                if word.isalnum() and not word.isdigit() and len(word) > 2:
                    for w in stop_words: #iterate through stop words
                        if w == word:
                            valid = False #if found not valid
                            break     
                    if valid == True: #if valid stem word and append to string text
                        word = stemmer.stem(word)
                        #text += word + ' ' #concatenate in loop
                        #text = ' '.join([text, word]) #join in loop
                        text.append(word) #append to list
            
            #write pmid and text string without last character since it is ' '
            #writeFile.write(article[0] + '\t' + ascii(text[:-1]) + '\n')
            #writeFile.write(article[0] + '\t' + ascii(text) + '\n') #using join in loop
            text = ' '.join(text)
            writeFile.write(article[0] + '\t' + ascii(text) + '\n') #using join at end
        
        writeFile.close()
        
        t1 = timeit.default_timer()
        print("Processing complete : " + os.path.basename(outFile) + " : " + str(t1 - t0))
        
# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='alter files in a directory to show articles pmid and stemmed text')
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputDirectory", help = "directory of output files")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

inputDirectory = args['inputDirectory']
outputDirectory = args['outputDirectory']

t2 = timeit.default_timer()
convertText(inputDirectory, outputDirectory)
t3 = timeit.default_timer()
print(t3 - t2)