"""
@author: kewilliams

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


def testValidArgs (descFile, suppFile, chemFile):
    
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
    notFoundCnt = 0 #count of terms not found
    
    t1 = timeit.default_timer()
    
    chemID = set() #set to remove duplicate IDs in chemical2pubtator file
    missingID = []
    
    for line in chemFile:
        #text[0] = PMID, text[1] = MeshID, text[2] = Mentions, text[3] = Resource
        text = line.split('\t') #only need text[1] and ignore CHEBI IDs
        if text[1] not in chemID and text[1][:5] != "CHEBI":
            chemID.add(text[1])
            #if not in sets
            if text[1] not in idSet:
                notFoundCnt += 1
                missingID.append([text[1], text[2]])
    
        #small test to show progress in reading of file
        loc += 1
        if loc % 5000000 == 0:
            t2 = timeit.default_timer()
            print(str(loc / 1000000) + " million terms tested: " + str(t2 - t1))
            t1 = timeit.default_timer()

    chemFile.close()
    
    print(str(notFoundCnt) + " terms not found in descriptor or supplemental files")
    
    return missingID


def createDict (descFile, suppFile):
    
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


def correctID (outFile, meshDict, missingID):
    
    print("Writing File...")
    writeFile = open(outFile, 'w')
    
    #i = 0
    notFound = []
    
    for item in missingID:
        
        found = False        
        text = item[1]
        #text[0] = ID, text[1] = terms separated by '|'
        words = text.split('|')
        for word in words: #iterate through words
            if word.lower() in meshDict: #if in descriptor dict
                #print(descDict[word.lower()] + '\t' + text[1])
                #write updated descriptor ID and original full string, remove {''} encapsulation from set
                writeFile.write(str(meshDict[word.lower()]).strip('{\'}') + '\t' + text + '\n')
                found = True
                break
            
        if found == False:
            #append not found ID and original string to notFound list
            notFound.append([item[0], item[1]])
            #print(word + " not found")
                
    #    i += 1
    #    if i == 20:
    #        break
             
    #write at bottom of file IDs and their terms that were not found
    writeFile.write("\nItems not found:\n")
    for item in notFound:
        writeFile.write(item[0] + '\t' + item[1] + '\n')
    
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

#create list of ids in chemical2pubtator that are not found in suppFile or descFile
missingID = compareSetToFile(idSet, chemFile)

#create dictionary containing data in descFile and suppFile
meshDict = createDict (descFile, suppFile)

#write file with corrected IDs
correctID(outFile, meshDict, missingID)

