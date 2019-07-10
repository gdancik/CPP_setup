# -*- coding: utf-8 -*-
"""
@author kewilliams

Usage:

  update_chemical2pubtator.py [-h] descriptorFile supplementalFile chemical2pubtator outFile

Code that compares known IDs in the descriptor and supplemental files against
chemical2pubtator IDs.  IDs in the chem2pubtator that are not found have their mentions
tested against the descriptor and supplemental mesh terms.  If there is a match, 
this ID is corrected to accurately reflect its mesh ID.

"""

import timeit
import argparse
import sys
from pathlib import Path
from collections import defaultdict


def testValidArgs(descFile, suppFile, chemFile):
    
    valid = True
    if not Path(descFile).is_file():
        print("Invalid descriptor file")
        valid = False
        
    if not Path(suppFile).is_file():
        print("Invalid supplemental file")
        valid= False
    
    if not Path(chemFile).is_file():
        print("Invalid chem2pubtator file")
        valid = False
    
    if valid == False:
        exit()


def createFileSet(descFile, suppFile):
    
    #set comprehension to take evaluated ascii ID ([0]) and add to set
    print("Reading descriptor IDs...")
    idSet = {eval(line.split('\t')[0]) for line in open(descFile)}
    
    print("Reading supplemental IDs...")
    suppID = {eval(line.split('\t')[0]) for line in open(suppFile)}
    
    #combine sets
    idSet.update(suppID)
    
    return idSet
    

def compareSetToFile(idSet, chemFile):
    
    print("Identifying bad IDs in chemical2pubtator...")    
    chemFile = open(chemFile)
    chemFile.readline() #remove header
    loc = 0 #location in file
    
    t1 = timeit.default_timer()
    
    missingDict = defaultdict(set)
    
    for line in chemFile:
        #text[0] = PMID, text[1] = MeshID, text[2] = Mentions, text[3] = Resource
        text = line.split('\t') #only need text[1] and ignore CHEBI IDs
        
        if text[1] not in idSet and text[1][:5] != "CHEBI":
            words = text[2].split('|') #separate mentions
            for word in words:
                missingDict[text[1]].add(word.lower())

        #small test to show progress in reading of file
        loc += 1
        if loc % 5000000 == 0:
            t2 = timeit.default_timer()
            print(str(loc / 1000000) + " million terms tested: " + str(t2 - t1))
            t1 = timeit.default_timer()

    chemFile.close()
    
    print(str(len(missingDict)) + " terms not found in descriptor or supplemental files")
    
    return missingDict


def createMeshDict(descFile, suppFile):
    
    print("Adding descriptor file to dictionary...")
    meshDict = {}
    for line in open(descFile):
        text = line.strip('\n').split('\t')
        for i in range(len(text) - 1):
            meshDict[eval(text[i + 1]).lower()] = eval(text[0])
    
    print("Adding supplemental file to dictionary...")
    for line in open(suppFile):
        text = line.strip('\n').split('\t')
        for i in range(len(text) - 1):
            meshDict[eval(text[i + 1]).lower()] = eval(text[0])
           
    return meshDict


def createUpdatedDict(meshDict, missingDict):
    
    found = False
    updatedDict = {}
    print("Creating dictionary with updated meshIDs...")    
    for meshID in missingDict:        
        words = missingDict[meshID]        
        for word in words: #iterate through words
            if word in meshDict: #if in descriptor dict
                found = True
                newID = meshDict[word]
                break
        if found == True:
            updatedDict[meshID] = newID
    
    print("Number of IDs to be updated:", len(updatedDict))
    return updatedDict
            
def writeCorrectedID(outFile, chemFile, updatedDict, idSet):    
    
    print("Writing updated file...")
    writeFile = open(outFile, 'w')
    loc = 0 #location in file
    t1 = timeit.default_timer()
    
    for line in open(chemFile):
        
        #text[0] = PMID, text[1] = MeshID, text[2] = Mentions, text[3] = Resource
        text = line.strip().split('\t') 
       
        #test to overwrite data from chemical2pubtator file
        if text[1] not in idSet and text[1][:5] != "CHEBI":
           
            replace = False
            if text[1] in updatedDict :
                meshID = updatedDict[text[1]]
                replace = True

            if replace == True:
                #replace the old meshID (text[1]) with new meshID
                writeFile.write(text[0] + '\t' + meshID + '\t' + \
                                text[2] + '\t' + text[3] + '\n')
            else: #if meshID not found in current descriptor or supplemental
                  #data but is also not in dictionary with updated info
                writeFile.write(line)
        
        else:
            writeFile.write(line)
        
        #small test to show progress in reading of file
        loc += 1
        if loc % 5000000 == 0:
            t2 = timeit.default_timer()
            print(str(loc / 1000000) + " million terms converted: " + str(t2 - t1))
            t1 = timeit.default_timer()
    
    writeFile.close()
    
    
#main code
ap = argparse.ArgumentParser(description='compare chem2pubtator IDs against descriptor and ' \
                             'supplemental IDs and correct outdated information')
ap.add_argument("descriptorFile", help = "file with descriptor ID information")
ap.add_argument("supplementalFile", help = "file with supplemental ID information")
ap.add_argument("chemical2pubtator", help = "chemical2pubtator file")
ap.add_argument("outFile", help = "file to output updated information to")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

descFile = args['descriptorFile']
suppFile = args['supplementalFile']
chemFile = args['chemical2pubtator']
outFile = args['outFile']

#test valid arguments
testValidArgs(descFile, suppFile, chemFile)

#create set of mesh ids
idSet = createFileSet(descFile, suppFile)

#create dict of ids in chemical2pubtator that are not found in suppFile or descFile
missingDict = compareSetToFile(idSet, chemFile)

#create dictionary containing data in descFile and suppFile
meshDict = createMeshDict(descFile, suppFile)

#create dictionary containing updated meshIDs and their words
updatedDict = createUpdatedDict(meshDict, missingDict)

#write new file with corrected IDs
writeCorrectedID(outFile, chemFile, updatedDict, idSet)

