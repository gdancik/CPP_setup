# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 12:32:23 2018

@author: kewil
"""

import timeit
t1 = timeit.default_timer()

inFile = "meshFile.txt"
searchTerm = ("Aggregates, Protein").lower()
found = False

t1 = timeit.default_timer()

for line in open(inFile):
    #text[0] = MeshTerm text[1+] are search terms
    text = line.strip('\n').split('\t')
    for i in range(len(text) - 1):
        if text[1 + i].lower() == searchTerm: #term names start at index 1
            print("MeshID = " + text[0])
            found = True
    if found == True:
        break

t2 = timeit.default_timer()
print(t2 - t1)