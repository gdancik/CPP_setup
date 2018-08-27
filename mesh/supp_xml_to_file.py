# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 13:33:59 2018

@author: kewil
"""

import xml.etree.ElementTree as ET

tree = ET.parse("supp2018.xml")

writeFile = open("suppFile.txt", 'w')

for record in tree.getiterator("SupplementalRecord"):
    
    writeFile.write(ascii(record.find("SupplementalRecordUI").text))
    #print(record.find("DescriptorUI").text + " - " + record.find("DescriptorName")[0].text)
    
    concepts = record.findall("ConceptList")
    for concept in concepts:
        termList = concept.findall("TermList") #list of all TermList
        for term in termList:
            for i in range(len(term)):
                writeFile.write('\t' + ascii(term[i].find("String").text)) #first string is descriptorName`
                #print(term[i].find("String").text)
    writeFile.write('\n')

writeFile.close()