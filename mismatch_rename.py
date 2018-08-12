# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 22:22:26 2018

@author: kewil
"""

print("adding descriptor file to dictionary")
descriptorFile = open("descFile.txt")
meshDict = {}

for line in descriptorFile:
    text = line.strip('\n').split('\t')
    for i in range(len(text) - 1):
        meshDict[eval(text[i + 1]).lower()] = set(eval(text[0]).split('\t'))

descriptorFile.close()

print("adding supplemental file to dictionary")
supplementalFile = open("suppFile.txt")

for line in supplementalFile:
    text = line.strip('\n').split('\t')
    for i in range(len(text) - 1):
        meshDict[eval(text[i + 1]).lower()] = set(eval(text[0]).split('\t'))
        
supplementalFile.close()

notFoundFile = open("chemicalNotFound.txt")
writeFile = open("correctedID.txt", 'w')

#i = 0
notFound = []

for line in notFoundFile:
    found = False
    #text[0] = ID, text[1] = terms separated by '|'
    text = line.strip('\n').split('\t')
    words = text[1].split('|')
    for word in words: #iterate through words
        if word.lower() in meshDict: #if in descriptor dict
            #print(str(meshDict[word.lower()]).strip('{\'}') + '\t' + text[1])
            #write updated descriptor ID and original full string
            writeFile.write(str(meshDict[word.lower()]).strip('{\'}') + '\t' + text[1] + '\n')
            found = True
            break

    if found == False:
        #append not found ID and original string to notFound list
        notFound.append([text[0], text[1]])
        #print(word + " not found")
            
#    i += 1
#    if i == 20:
#        break
            
notFoundFile.close()
         
#write at bottom of file IDs and their terms that were not found
writeFile.write("\nItems not found:\n")
#print()
#print("Items not found:")
#print()
for item in notFound:
    #print(item[0] + '\t' + item[1])
    writeFile.write(item[0] + '\t' + item[1] + '\n')

writeFile.close()