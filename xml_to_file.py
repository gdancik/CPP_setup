# -*- coding: utf-8 -*-
"""
Usage:

  xml_to_file.py [-h] inputFile outputFile fileType(descriptor/supplementary)

Code to read either a descriptor or supplementary xml file and retrieve the mesh ID
and mesh terms.

"""

import argparse
import sys
import xml.etree.ElementTree as ET

def validFileType(fileType):
    if fileType != "descriptor" and fileType != "supplementary":
        print("Invalid File Type")
        exit()

def xmlParse(inputFile, outputFile, fileType):
    
    tree = ET.parse(inputFile)
    
    writeFile = open(outputFile, 'w')
    
    if fileType == "descriptor":
        recordString = "DescriptorRecord"
        recordUIString = "DescriptorUI"
        
    elif fileType == "supplementary":
        recordString = "SupplementalRecord"
        recordUIString = "SupplementalRecordUI"
    
    for record in tree.getiterator(recordString):
        
        writeFile.write(ascii(record.find(recordUIString).text))
        
        concepts = record.find("ConceptList") #terms located in conceptList branch
        for concept in concepts:
            termList = concept.findall("TermList") #list of all TermList
            for term in termList:
                for i in range(len(term)): #iterate through all terms, write to file
                    writeFile.write('\t' + ascii(term[i].find("String").text))
        writeFile.write('\n')
    
    writeFile.close()

ap = argparse.ArgumentParser(description='retrieve meshID and meshterms from xml file')
ap.add_argument("inputFile", help = "xml file to be parsed")
ap.add_argument("outputFile", help = "name of text file to be output")
ap.add_argument("fileType", help = "type of xml file (descriptor or supplementary)")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

inputFile = args['inputFile']
outputFile = args['outputFile']
fileType = args['fileType'].lower()

validFileType(fileType)

xmlParse(inputFile, outputFile, fileType)

