# -*- coding: utf-8 -*-
"""
@author: kewilliams

Usage:

  xml_to_file.py [-h] inputFile outputFile 

Code to read pa2019.xml and output the recordUI and recordName 
and mesh terms.

"""

import argparse
import sys
import xml.etree.ElementTree as ET

def xmlParse(inputFile, outputFile):
    
    tree = ET.parse(inputFile)
    
    writeFile = open(outputFile, 'w')
   
    for record in tree.getiterator('Substance'):
        
#        writeFile.write(ascii(record.find(recordUIString).text))
        id = record.find('RecordUI') 
        if id == None :
            continue
        name = record.find('RecordName')
        if name == None :
            continue
        name = name.find('String')
        if name == None :
            continue
        
        print(id.text + '\t' + name.text)

    #    writeFile.write('\t' + ascii(term[i].find("String").text))
    
   # writeFile.close()

ap = argparse.ArgumentParser(description='retrieve meshID and meshterms from xml file')
ap.add_argument("inputFile", help = "xml file to be parsed")
ap.add_argument("outputFile", help = "name of text file to be output")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

inputFile = args['inputFile']
outputFile = args['outputFile']


xmlParse(inputFile, outputFile)

