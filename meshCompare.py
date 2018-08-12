# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 17:01:24 2018

@author: kewil
"""

import timeit

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
notFound = 0 #count of terms not found

t1 = timeit.default_timer()
t3 = timeit.default_timer()

print("Testing chemical2pubtator against current IDs...")
chemID = set() #set to remove duplicate IDs in chemical2pubtator file
for line in chemFile:
    #text[0] = PMID, text[1] = MeshID, text[2] = Mentions, text[3] = Resource
    text = line.split('\t') #only need text[1]
    if text[1] not in chemID and text[1][:5] != "CHEBI":
        chemID.add(text[1])
        #if not in sets
        if text[1] not in setID:
            notFound += 1                
            writeFile.write(text[1] + '\t' + text[2] + '\n')
            #print(text[0] + '\t' + text[2] + " not found")

    #small test to show progress in reading of file
    loc += 1
    if loc % 5000000 == 0:
        t2 = timeit.default_timer()
        print(str(loc / 1000000) + " million terms tested: " + str(t2 - t1))
        t1 = timeit.default_timer()

writeFile.close()
chemFile.close()

t4 = timeit.default_timer()

print(str(notFound) + " terms not found in descriptor or supplemental files")

