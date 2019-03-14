#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 08:14:21 2018

@author: dancikg
"""

import os
import glob
import argparse
import sys

# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Extract PMIDs from all *.txt files in a directory')
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputFile", help = "name of output file")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

directory = args['inputDirectory']
outFile = args['outputFile']

# create file listing all PMIDs for text files in directory
fileNames = glob.glob(directory+"/*.txt")

allPMIDs = []

for file in fileNames :
    #print("reading file", file)
    f = open(file)
    pmids = [eval(l.split("\t")[0]) for l in f]
    allPMIDs = allPMIDs + pmids
    f.close()

f = open(outFile, "w")
[f.write(x+"\n") for x in allPMIDs]
f.close()

print(len(allPMIDs), "pmids written to file: ", outFile)
