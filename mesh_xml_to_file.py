# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 12:18:14 2018

@author: kewil
"""

import xml.etree.ElementTree as ET

tree = ET.parse("desc2018.xml")

writeFile = open("descFile.txt", 'w')

for record in tree.getiterator("DescriptorRecord"):
    
    writeFile.write(ascii(record.find("DescriptorUI").text))
    #print(record.find("DescriptorUI").text + " - " + record.find("DescriptorName")[0].text)
    
    concepts = record.find("ConceptList")
    for concept in concepts:
        termList = concept.findall("TermList") #list of all TermList
        for term in termList:
            for i in range(len(term)):
                writeFile.write('\t' + ascii(term[i].find("String").text)) #first string is descriptorName`
                #print(term[i].find("String").text)
    writeFile.write('\n')

writeFile.close()
    