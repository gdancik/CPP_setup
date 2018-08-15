# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 17:01:24 2018

@author: kewilliams
"""

import timeit
from collections import defaultdict

#set comprehension to take evaluated ascii ID ([0]) and add to set
print("Reading descriptor IDs")
setID = {eval(line.split('\t')[0]) for line in open("descFile.txt")}

print("Reading supplemental IDs")
suppID = {eval(line.split('\t')[0]) for line in open("suppFile.txt")}

#combine sets
setID.update(suppID)

writeFile = open("chemicalNotFound.txt", 'w') #file to write to
chemFile = open("chemical2Pubtator")

chemFile.readline() #remove header

loc = 0 #location in file

t1 = timeit.default_timer()
missingDict = defaultdict(set)

print("Testing chemical2pubtator against current IDs...")
chemID = set() #set to remove duplicate IDs in chemical2pubtator file
for line in chemFile:
    #text[0] = PMID, text[1] = MeshID, text[2] = Mentions, text[3] = Resource
    text = line.split('\t') #only need text[1]
    
    if text[1] not in setID and text[1][:5] != "CHEBI":
        
        words = text[2].split('|') #separate mentions
        for word in words:
            missingDict[text[1]].add(word.lower())

    #small test to show progress in reading of file
    loc += 1
    if loc % 5000000 == 0:
        t2 = timeit.default_timer()
        print(str(loc / 1000000) + " million terms tested: " + str(t2 - t1))
        t1 = timeit.default_timer()

for item in missingDict:
    writeFile.write(item + '\t' + '|'.join(missingDict[item]) + '\n')
writeFile.close()
chemFile.close()