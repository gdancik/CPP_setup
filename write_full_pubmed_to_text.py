# -*- coding: utf-8 -*-
"""
Usage:

  write_full_pubmed_to_text.py [-h] username password inputDirectory outputDirectory

Extract dcast article information from PubMed xml files

positional arguments:
  username         dcast username
  password         dcast password
  inputDirectory   directory of input files
  outputDirectory  directory of output files

Tests against dcast database for matching pmids in the PubGene table
"""
#possible try/catch imports
import lxml #to catch XMLSyntaxError
import shutil #move file location

import pubmed_parser as pp
import timeit
import time
import mysql.connector
from mysql.connector import errorcode

import sys
import argparse
import glob
import os


#parse xml into dictionary
def createPubDict (file):
    pubmed_dict = pp.parse_medline_xml(file)
    return pubmed_dict

#database access for pmids
def dCastDatabase (userName, password, inputDirectory, outputDirectory):
    try:
        cnx = mysql.connector.connect(user=userName, password=password,
                                      database='dcast')
    except mysql.connector.Error as err:
        
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        #if valid connection to database, create txt files
        createTxtFromXML(inputDirectory, cnx)
        cnx.close()

def createTxtFromXML(filePath, cnx):    

    query = ("select PMID from PubGene where PMID = ") #generic query
    errorStr = "" #for try / catch
    
    # get all xml.gz files in specified directory
    files = sorted(glob.glob(filePath +"/*.xml.gz"))
    print("Number of *.xml.gz files found in directory '", filePath, "': ", len(files), sep = "")

    # create outputDirectory if it does not exist
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    errorCount = 0

    for inFile in files:
        t0 = timeit.default_timer()
        
        try:
            #create dictionary from retrieved xml.gz
            pubmed_dict = createPubDict(inFile)
        
        except :            
            if not os.path.exists(outputDirectory + ("/ERRORS/")): #create folder for failed file
                os.makedirs(outputDirectory + ("/ERRORS/"))
            shutil.copy(inFile, outputDirectory + "/ERRORS/" + os.path.basename(inFile)) #move to ERROR folder
            errorStr = os.path.basename(inFile) + " - " + str(sys.exc_info()[0])
            print(errorStr)
            f = open(outputDirectory + "/ERRORS/log.txt", "a")
            f.write(errorStr + "\n")
            f.close()
            errorCount += 1
            continue #skip to next file
        
             
        outFile = outputDirectory + "/extracted_" + os.path.basename(inFile).replace(".xml.gz", ".txt")
        
        writeFile = open(outFile, 'w') #open file for data transfer
        
        #unbuffered fetchone() causes error after a large amount of queries, reusing a cursor
        #repeatedly without fetching all results leads to "unread result found"
        #buffered allows all results to be fetched, but only returns one to code
        cursor = cnx.cursor(buffered=True)
        
        for item in pubmed_dict:
            if item['delete'] != 'False': #if entry not updated later
                cursor.execute(query + item['pmid']) #query + current items pmid
                row = cursor.fetchone() #fetches result of query, either None or matching value
                if row != None : #if matching value found
                     writeToFile(item, writeFile) #write item in pubmed_dict to file
        writeFile.close() #next iteration will be new file name, this file is no longer used
        cursor.close()
        t1 = timeit.default_timer()
        print("Successful Write : " + outFile + " : " + str(t1 - t0))   
        time.sleep(1)
    
    #unnecessary unless try / catch 
    if errorCount is not 0 :
        print("\nWarning:", errorCount, "files could not written. See", outputDirectory + "/ERRORS/log.txt for more information")


def writeToFile (item, writeFile):

    writeFile.write(ascii(item['pmid']) + '\t' + 
                    ascii(item['title']) + '\t' + 
                    ascii(item['author']) + '\t' + 
                    ascii(item['journal']) + '\t' +
                    ascii(item['pubdate']) + '\t' + 
                    ascii(item['abstract']) + '\n')
    

# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Extract dcast article information from PubMed xml files')
ap.add_argument("username", help="dcast username")
ap.add_argument("password", help="dcast password")
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputDirectory", help = "directory of output files")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

userName = args['username']
password = args['password']

inputDirectory = args['inputDirectory']
outputDirectory = args['outputDirectory']

#path for xml and text files, only necessary change for user
dCastDatabase(userName, password, inputDirectory, outputDirectory)