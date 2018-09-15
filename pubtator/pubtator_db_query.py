# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:50:49 2018

@author: kewilliams

Usage:

    python pubtator_db_query.py [-h] username password pubType inputFile outDirectory

To deal with multiple file types, parameter pubType is used
should be able to handle gene, disease, chemical and mutation

Can be updated for other pubtator files by altering getFileTypeInfo
If multiple queries needed can return an additional query string there
use null or "" if only one query needed and test for it in getPubSet

Creating multiple sets will probably require a new function
"""

import mysql.connector
from mysql.connector import errorcode
import os
import sys
import argparse

def getFileTypeInfo(pubType, outDir): #update for more pubtator filetypes
    
    if not outDir.endswith('/'):
        outDir += '/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    if pubType == "gene":
        query = ("select GeneID from Genes")
        outFile = outDir + "gene2pubtator_processed"
    else:
        print("Unknown pubtator file type")
        exit()
        
    return query, outFile
        

def dCastDatabase (userName, password):
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
        return cnx


def getPubSet(cnx, query):
    
    print("Creating set...")    
    cursor = cnx.cursor()
    cursor.execute(query)
    pubSet = {x[0] for x in cursor.fetchall()} #fetches are a single value tuple
    #print(pubSet)
    print(str(len(pubSet)) + " items in set")
    return pubSet


def writeToFile(pubSet, inFile, outFile):
    
    matchCnt = 0 #counter for number of files written
    lineCnt = 0 #counter to display progress in code
    
    readFile = open(inFile)    
    writeFile = open(outFile, 'w')
    print("Reading pubtator file...")
    #writeFile.write(readFile.readline().strip() + '\n')
    line = readFile.readline()
    writeFile.write(line.strip() + '\n')
    for line in readFile:
        lineCnt += 1
        text = line.strip().split('\t')
        if eval(text[1]) in pubSet:
            matchCnt += 1
            writeFile.write(line.strip() + '\n')
        
        if lineCnt % 1000000 == 0:
            print(str(lineCnt) + " lines read")
            
    print(str(lineCnt) + " total lines read")
    print(str(matchCnt) + " genes written to file")
    writeFile.close()
    

ap = argparse.ArgumentParser(description='Extract dcast article information from PubMed xml files')
ap.add_argument("username", help="dcast username")
ap.add_argument("password", help="dcast password")
ap.add_argument("pubType", help="pubtator processed file type (gene etc)")
ap.add_argument("inputFile", help = "input files name")
ap.add_argument("outputDirectory", help = "directory of output files")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

userName = args['username']
password = args['password']
pubType = args['pubType']
inFile = args['inputFile']
outDir = args['outputDirectory']


output = getFileTypeInfo(pubType, outDir) #get tailored info for putator filetype
query = output[0] #query for database
outFile = output[1] #output file name

cnx = dCastDatabase(userName, password)  #get to database
pubSet = getPubSet(cnx, query) #get set of wanted values from database
writeToFile(pubSet, inFile, outFile) #write data to file

cnx.close() #close connection