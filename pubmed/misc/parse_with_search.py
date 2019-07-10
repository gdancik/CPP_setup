"""
@author: kewilliams
"""

#probably will reorganize because you won't necessarily be searching for all keywords
#in theory you would target a specific one, but this is a general outline on what to do

import pubmed_parser as pp
import re

#read file into a table
def createSynTable(inFile):
   
    index = 0
    for line in open(inFile):
        if index == 0: #if first line in file
            synTable = [[]] #create empty table
            synTable[index] = line.split('\t') #add first line to new table
        else:
            synTable.append([]) #add new line to table
            synTable[index] = line.split('\t') #add line
        index += 1

    return synTable

#doing regex with strings from text file yielded inaccurate matches.  "wes" will
#be found in the string "western".  To eliminate, add additional column in table
#with word boundaries.  This unfortunately also removes the plurals such as mutations
def addRegexString(synTable):

    index = 0
    for entry in synTable: #for each row
        tempList = synTable[index][2].strip().split('|') #turn to list
        tempStr = ""
        for item in tempList: #surround each word in list with \b and separate with '|'
            tempStr += "\\b" + item + "\\b|"
        synTable[index].append(tempStr[:-1]) #append new string with boundaries
        index += 1
    return synTable

#print matches in sample dictionary to console
def found(pubmed_dict, synTable):
    
    count = 1 #for testing to see how many matches
    for article in pubmed_dict: #iterate through articles
        for index in range(len(synTable)): #iterate through each search string
            find = synTable[index][3] #string with regex word boundaries
            
            text = article['abstract'] #abstract to search
            #find regex string, ignore case sensitivity
            regex = re.findall(find, text, re.IGNORECASE)
            if regex: #if found
                print(article['pmid'] + '\t' + synTable[index][0])
                print(regex)
                print(count)
                count += 1

synFile = "synonyms.txt"
pubmed_dict = pp.parse_medline_xml('pubmedsample18n0001.xml')

synTable = createSynTable(synFile) #create synonym table
synTable = addRegexString(synTable) #add new regex string to table

found(pubmed_dict, synTable)
            
            