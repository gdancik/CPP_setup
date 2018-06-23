# -*- coding: utf-8 -*-
"""
Usage:

  convert_cancer_related.py [-h] username password inputDirectory outputDirectory

Extract dcast article information from PubMed xml files

positional arguments:
  username         dcast username
  password         dcast password
  inputDirectory   directory of input files
  outputDirectory  directory of output files

Takes text files with pubmed pmid matches and creates new files that are
only cancer related
"""

import mysql.connector
from mysql.connector import errorcode

import timeit
import sys
import argparse
import glob
import os

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
        createCancerTxt(inputDirectory, cnx)
        cnx.close()

def createCancerTxt(filePath, cnx):
    
    #generic query - split into two parts, before and after changing value
    query1 = "select distinct PMID from PubMesh inner join MeshTerms ON " + \
        "PubMesh.MeshID = MeshTerms.MeshID where PubMesh.PMID = "
    query2 = " and TreeID like \"C04.%\"";
    
    #get all text files from location
    files = sorted(glob.glob(filePath +"/*.txt"))
    
    # create outputDirectory if it does not exist
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    
    for inFile in files:
        t0 = timeit.default_timer()
        outFile = outputDirectory + "/cancer_" + os.path.basename(inFile) #alter name to show for cancer
        writeFile = open(outFile, 'w')
        
        cursor = cnx.cursor(buffered=True)
        
        for line in open(inFile):
            article = line.split('\t') #turn line to tab deliminated list
            cursor.execute(query1 + eval(article[0]) + query2) #article in ascii format
            row = cursor.fetchone() #check for at least one match
            if row != None: #if found
                writeFile.write(line) #write line to new file
        writeFile.close()
        cursor.close()
        t1 = timeit.default_timer()
        print(os.path.basename(inFile) + " successfully updated : " + str(t1 - t0))
            
        
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