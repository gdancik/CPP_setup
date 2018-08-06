# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 13:06:35 2018

@author: kewil
"""

import xml.etree.ElementTree as ET

tree = ET.parse("desc2018.xml")
#root = tree.getroot()
    
#children = root.getchildren()
#c = children[0]
#cl = c.findall("ConceptList")

# get terms from ConceptList


#iterate through children
#first.find("DescriptorUI").text = D########
#first.find("DescriptorName")[0].text = Descriptor Name #need [0] otherwise '\n    ' returned

#concept = first.find("ConceptList")
#concept = concept[0] #only one branch in concept, need to move down tree

#may have multiple termlists

#termList = concept.findall("TermList") #list of termLists, need to iterate

#first term list
#for i in range(len(firstTermList)):
#   print(firstTermList[i].find("String").text)


#i = 0
#
#for record in tree.getiterator("DescriptorRecord"):
#    
#    print(record.find("DescriptorUI").text + " - " + record.find("DescriptorName")[0].text)
#    
#    concept = record.find("ConceptList")[0]
#    termList = concept.findall("TermList") #list of all TermList
#    for term in termList:
#        for i in range(len(term)):
#            print(term[i].find("String").text)
#            
#    if i == 20: #cutoff to prevent full iteration for testing
#        break
#    else:
#        print()
#        i += 1

searchTerm = ("Bladder neoplasms").lower()
found = False        

for record in tree.getiterator("DescriptorRecord"):
    
    meshTerm = record.find("DescriptorUI").text
    
    concept = record.find("ConceptList")[0]
    termList = concept.findall("TermList") #list of all TermList
    for term in termList:
        for i in range(len(term)):
            string = term[i].find("String").text
            if string.lower() == searchTerm:
                print(meshTerm)
                found = True
    if found == True:
        break
