# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 13:06:35 2018

@author: kewil
"""

import xml.etree.ElementTree as ET
import timeit

t1 = timeit.default_timer()

tree = ET.parse("desc2018.xml")
#root = tree.getroot()
    
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

searchTerm = ("Erlotinib").lower()
found = False

for record in tree.getiterator("DescriptorRecord"):
    
    meshTerm = record.find("DescriptorUI").text
    concepts = record.find("ConceptList")
    for concept in concepts:
        
        termList = concept.findall("TermList") #list of all TermList
        for term in termList:
            for i in range(len(term)):
                string = term[i].find("String").text
                if string.lower() == searchTerm:
                    print(meshTerm)
                    found = True
        
    if found == True:
        break
t2 = timeit.default_timer()
print(t2 - t1)