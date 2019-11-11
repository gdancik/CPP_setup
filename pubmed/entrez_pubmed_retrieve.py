# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 09:11:39 2018

@author: kewilliams

usage:
    
    entrez_pubmed_retrieve.py [-h] pmidFile outDirectory email
    
Takes file containing pmids and queries them against the pubmed database in batches of 
500.  Retrieve pmid, title, author, journal, publish year, and abstract and formats
them to match data already present in database

positional arguments:
    pmidFile - file containing pmids to be queried
    outDirectory - directory for output files
    email - email for Entrez

"""

from Bio import Entrez
from Bio import Medline

import time
import os
import sys
import argparse
from pathlib import Path


def testPmidFile(pmidFile):
    if not Path(pmidFile).is_file():
        print("Invalid pmidFile")
        exit()

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
        if len(name) > 1 :
            givenName = name[1].split()
            #take and join first letter in each given name
            initials = ''.join([item[0] for item in givenName])
        else :
            initials = ''
        authorList.append(initials + ' ' + name[0]) #add initials and surname
        authors = '; '.join(authorList) #join authors with ; separation
    
    return authors


def readFile (pmidFile, outDir):
    
    #verify directory ends with '/' and create directory if doesnt exist
    if not outDir.endswith('/'):
        outDir += '/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    number = 1 #tracker to identify new files for each query

    idList = [i.strip() for i in open(pmidFile).readlines()] #readlines in file, strip '\n'
        
    while len(idList) != 0: #while list is not empty

        outFile = outDir + "entrez_query_" + str(number) + ".txt" #file name
        print("Writing file: " + outFile)
        number += 1 #increment file number
        entrezQuery(idList[:500], outFile) #query first 500
        idList = (idList[500:]) #remove first 500
        time.sleep(1) #wait 1 second
        if number % 5 == 0 :
            time.sleep(1)

#outDir = r"C:/Users/kewil/test/pmid/"
#pmidFile = r"C:/Users/kewil/Summerbio/misc_data_files/pmids.txt"

ap = argparse.ArgumentParser(description="query selected pmids against pubmed db")
ap.add_argument("pmidFile", help="designated file containing pmids")
ap.add_argument("outDirectory", help="output directory for query files")
ap.add_argument("email", help="email for entrez queries")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

pmidFile = args['pmidFile']
outDir = args['outDirectory']
entrezEmail = args['email']

testPmidFile(pmidFile)
Entrez.email = entrezEmail
readFile(pmidFile, outDir)
