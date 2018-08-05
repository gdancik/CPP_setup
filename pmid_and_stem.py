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

import string
import glob
import argparse
import sys
import os
import timeit

from words import stemWords

def convertText(inputDirectory, outputDirectory):
    
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

            text = stemWords(text)

            #write pmid and text string without last character since it is ' '
            #writeFile.write(article[0] + '\t' + ascii(text[:-1]) + '\n')
            #writeFile.write(article[0] + '\t' + ascii(text) + '\n') #using join in loop

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
