# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 17:01:24 2018

@author: kewil
"""

import timeit

print("creating descriptor ID list")
#descFile = open("descFile.txt")
descID = [eval(line.strip('\n').split('\t')[0]) for line in open("descFile.txt")]

#descID = []
#for line in descriptorFile:
#    text = line.strip('\n').split('\t')
#    descID.append(eval(text[0])) #list of descriptor IDs

#descFile.close()

print("creating supplemental ID list")
#suppFile = open("suppFile.txt")
suppID = [eval(line.strip('\n').split('\t')[0]) for line in open("suppFile.txt")]

#suppID = []
#for line in supplementalFile:
#    text = line.strip('\n').split('\t')
#    suppID.append(eval(text[0]))
        
#suppFile.close()

writeFile = open("chemicalNotFound.txt", 'w') #file to write to
chemFile = open("chemical2Pubtator")

chemFile.readline() #remove header

loc = 0 #location in file
notFound = 0 #count of terms not found

t1 = timeit.default_timer()

print("testing chemical2pubtator against dictionaries")
chemID = [] #list to remove duplicate IDs in chemical2pubtator file
for line in chemFile:
    #text[0] = PMID, text[1] = MeshID, text[2] = Mentions, text[3] = Resource
    text = line.split('\t') #only need text[1]
    if text[1] not in chemID and text[1][:5] != "CHEBI":
        chemID.append(text[1])
        if text[1] not in descID:
            if text[1] not in suppID:
                notFound += 1                
                #write MeshID \t Mentions \n
                writeFile.write(text[1] + '\t' + text[2] + '\n')
                #print(text[0] + '\t' + text[2] + " not found")

    #small test to show progress in reading of file
    loc += 1
    if loc % 500000 == 0:
        t2 = timeit.default_timer()
        print(str(loc) + " terms tested: " + str(t2 - t1))
        t1 = timeit.default_timer()

writeFile.close()
chemFile.close()

print(str(notFound) + " terms not found in descriptor or supplemental files")