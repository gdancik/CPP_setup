# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 09:11:39 2018

@author: kewilliams

usage:
    
    retrieve_title_abstract.py [-h] pmidFile outDirectory
    
Takes file containing pmids and queries them against the pubmed database in batches of 
500.  Retrieve pmid, title, author, journal, publish year, and abstract and formats
them to match data already present in database

positional arguments:
    pmidFile - file containing pmids to be queried
    outDirectory - directory for output files

"""

from Bio import Entrez
from Bio import Medline

import time
import os
import sys
import argparse

Entrez.email = "kewilliams86@gmail.com"


def entrezQuery(idList, outFile):
    
    writeFile = open(outFile, 'w')
    
    handle = Entrez.efetch(db="pubmed", id=idList, rettype="medline", retmode="text")
    records = Medline.parse(handle)
    for record in records:
        #either return record entry or empty string
        pmid = record.get('PMID', '')
        title = record.get('TI', '')
        authors = record.get('FAU', '')
        authors = modifyAuthors(authors) #format authors
        journal = record.get('JT', '')
        date = record.get('DP', '')
        date = date[0:4] #year only
        abstract = record.get('AB', '')
        #need ascii encapsulation for uniformity with database
        writeFile.write(ascii(pmid) + '\t' + ascii(title) + '\t' + ascii(authors) + '\t' +
                        ascii(journal) + '\t' + ascii(date) + '\t' + ascii(abstract) + '\n')

#from baseline authors are formatted FirstInit '' MidInit ' ' LastName '; '
#eztrez records returns a list of LastName, givenName givenName...
def modifyAuthors(authors):
    
    authorList = []
    for author in authors:
        name = author.split(',') #split at comma since last names may have multiple words
        givenName = name[1].split()
        #take and join first letter in each given name
        initials = ''.join([item[0] for item in givenName])
        authorList.append(initials + ' ' + name[0]) #add initials and surname
    authors = '; '.join(authorList) #join authors with ; separation
    
    return authors


def readFile (pmidFile, outDir):
    
    #verify directory ends with '/' and create directory if doesnt exist
    if not outDir.endswith('/'):
        outDir += '/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    count = 0 #tracker for time.sleep to stagger entrez queries
    number = 1 #tracker to identify new files for each query
    idList = [] #list of ids to be queried, chunk by 500 or less
    
    for line in open(pmidFile):
        idList.append(line.strip())
        count += 1
        if count % 500 == 0: #when 500 ids in list
            outFile = outDir + "entrez_query_" + str(number) + ".txt"
            entrezQuery(idList, outFile) #query and write file
            idList = [] #reset idList 
            number += 1 #increase number for entrez query
            time.sleep(1) #sleep
            
    if count % 500 != 0: #if remainder of files in idList
        outFile = outDir + "entrez_query_" + str(number) + ".txt"
        entrezQuery(idList, outFile) #query and write file


#outDir = r"C:/Users/kewil/test/pmid/"
#pmidFile = r"C:/Users/kewil/Summerbio/misc_data_files/pmids.txt"

ap = argparse.ArgumentParser(description="Query selected pmids against pubmed db")
ap.add_argument("pmidFile", help="designated file containing pmids")
ap.add_argument("outDirectory", help="output directory for query files")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

pmidFile = args['pmidFile']
outDir = args['outDirectory']

readFile(pmidFile, outDir)