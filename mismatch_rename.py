# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 22:22:26 2018

@author: kewil
"""

print("creating descriptor file dictionary")
descriptorFile = open("descFile.txt")
descDict = {}

for line in descriptorFile:
    text = line.strip('\n').split('\t')
    for i in range(len(text) - 1):
        descDict[eval(text[i + 1]).lower()] = eval(text[0]).lower()

descriptorFile.close()

print("creating supplemental file dictionary")
supplementalFile = open("suppFile.txt")
suppDict = {}

for line in supplementalFile:
    text = line.strip('\n').split('\t')
    for i in range(len(text) - 1):
        suppDict[eval(text[i + 1]).lower()] = eval(text[0])
        
supplementalFile.close()

notFoundFile = open("chemicalNotFound.txt")
writeFile = open("correctedID.txt", 'w')

#i = 0
notFound = []

for line in notFoundFile:
    #text[0] = ID, text[1] = terms separated by '|'
    text = line.strip('\n').split('\t')
    words = text[1].split('|')
    for word in words: #iterate through words
        if word.lower() in descDict: #if in descriptor dict
            #print(descDict[word.lower()] + '\t' + text[1])
            #write updated descriptor ID and original full string
            writeFile.write(descDict[word.lower()] + '\t' + text[1] + '\n')
            break
        elif word.lower() in suppDict:
            #print(suppDict[word.lower()] + '\t' + word)
            #write updated supplemental ID and original full string
            writeFile.write(suppDict[word.lower()] + '\t' + text[1] + '\n')
            break
        else:
            #append not found ID and original string to notFound list
            notFound.append([text[0], text[1]])
            #print(word + " not found")
            
#    i += 1
#    if i == 20:
#        break
            
notFoundFile.close()
         
#write at bottom of file IDs and their terms that were not found
writeFile.write("\nItems not found:\n")
for item in notFound:
    writeFile.write(item[0] + '\t' + item[1] + '\n')

writeFile.close()