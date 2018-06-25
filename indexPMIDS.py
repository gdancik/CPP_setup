#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 13:05:25 2018

@author: dancikg
"""

import argparse
import glob
import sys
import gzip
import os

# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Create an "index" file for all pubmed baseline PMIDs in directory')
ap.add_argument("directory", help="directory containing *.xml.gz files")
ap.add_argument("outFile", help="name of output file")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

directory = args['directory']
outFile = args['outFile']

count = 1
files = glob.glob(directory + "/*.xml.gz")
for fileName in files :
    print("parsing file #", count, ":", os.path.basename(fileName))
    count+=1
    file = gzip.open(fileName, "rt")
    try : 
        lines = file.readlines()
    except :
        ferror = open("log.txt", "a")
        ferror.write(fileName + "\n")
        ferror.close()
        continue
    
    lines = [l for l in lines if "<PMID" in l]        

    fout = open(outFile, "a")
    fileName = os.path.basename(fileName)
    for l in lines :
        fout.write(fileName + ": " + l.lstrip())
    fout.close()
    
