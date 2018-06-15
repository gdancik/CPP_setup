# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 21:36:36 2018

@author: kewil
"""
import pubmed_parser as pp
import urllib.request

#parse xml into dictionary
def createPubDict (file):
    pubmed_dict = pp.parse_medline_xml(file)
    return pubmed_dict

def retrieveFiles():
    url = "ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
    
    #path for xml and text files
    directory = "C:/Users/kewil/PubMedXML/"
    
    numStop = 930 # use to get all abstracts
    numStop = 5   # use for testing
    
    for fileNum in range(1, numStop) :
        fileNumStr = str(fileNum)
        fileNumStr = fileNumStr.rjust(4, "0")  # pad string with 0s
    
        fileName = "pubmed18n" + fileNumStr + ".xml.gz"
        print("retrieving file:", fileName)
        
        outFile = directory + "extracted_pubmed18n" + fileNumStr + ".txt"
        
        #Needed encoding='utf-8' to prevent UnicodeEncodeErrors
        writeFile = open(outFile, 'w', encoding='utf-8')
        urllib.request.urlretrieve(url + fileName, directory + fileName)
        
        #create dictionary from retrieved xml.gz
        pubmed_dict = createPubDict("C:/Users/kewil/PubMedXML/"+fileName)
        print("writing file:", "extracted_" + fileName[:-6] + "txt")
        for item in pubmed_dict:
            writeToFile(item, writeFile) #write desired info to file
        writeFile.close()

def writeToFile (item, writeFile):
    writeFile.write(item['pmid'] + '\t' + item['title'] + '\t' + 
                    item['author'] + '\t' + item['journal'] + '\t' +
                    item['pubdate'] + '\t' + item['abstract'] + '\n')
    

retrieveFiles()