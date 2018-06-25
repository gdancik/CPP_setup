#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 08:14:21 2018

@author: dancikg
"""

import os
import glob


# create file listing all PMIDs for text files in directory
directory = "CPP_articles"
fileNames = glob.glob(directory+"/*.txt")

allPMIDs = []

for file in fileNames :
    #print("reading file", file)
    f = open(file)
    pmids = [eval(l.split("\t")[0]) for l in f]
    allPMIDs = allPMIDs + pmids
    f.close()

f = open("pmids.txt", "w")
[f.write(x+"\n") for x in allPMIDs]
f.close()



