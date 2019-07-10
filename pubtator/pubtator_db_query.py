# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:50:49 2018

@author: kewilliams

Usage:

    python pubtator_db_query.py [-h] username password pubType inputFile outDirectory

Currently handles gene, disease, or chemical
"""

import mysql.connector
from mysql.connector import errorcode
import os
import sys
import argparse
import timeit

def getFileTypeInfo(pubType, outDir): #update for more pubtator filetypes
    
    if not outDir.endswith('/'):
        outDir += '/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    if pubType == "gene":
        query = "select GeneID from Genes"
        outFile = outDir + "gene2pubtator_updated"
    elif pubType == "chemical":
        query = "select MeshID from pubchem"
        outFile = outDir + "chemical2pubtator_updated"
    elif pubType == "disease":
        query = "select MeshID from pubmesh"
        outFile = outDir + "disease2pubtator_updated"
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


#genes were encapsulated with '' in the file, disease and chemical were not
def pubTest(pubType, pubSet, text):
    
    test = False
    
    if pubType == "chemical" or pubType == "disease":
        if text in pubSet:
            test = True
    if pubType == "gene":
        if int(text) in pubSet:
            test = True
    
    return test

def writeToFile(pubSet, pubType, inFile, outFile):
    
    t1 = timeit.default_timer()
    matchCnt = 0 #counter for number of files written
    lineCnt = 0 #counter to display progress in code
    
    readFile = open(inFile)    
    writeFile = open(outFile, 'w')
    print("Reading pubtator file...")
    writeFile.write(readFile.readline().strip() + '\n')
    
    for line in readFile:
        lineCnt += 1
        text = line.strip().split('\t')
        if not line.strip() == "": #some lines contained only "" or "\n"
            if pubTest(pubType, pubSet, text[1]) == True: #calls function to test validity
                matchCnt += 1
                writeFile.write(line.strip() + '\n')        
        if lineCnt % 1000000 == 0:
            print(str(lineCnt) + " lines read")            
#        if matchCnt == 10000:
#            break
    print(str(lineCnt) + " total lines read")
    print(str(matchCnt) + " items written to file")
    writeFile.close()
    
    t2 = timeit.default_timer()
    print("completion time: " + str(t2 - t1))
    

ap = argparse.ArgumentParser(description='Extract dcast article information from PubMed xml files')
ap.add_argument("username", help="dcast username")
ap.add_argument("password", help="dcast password")
ap.add_argument("pubType", help="pubtator processed file type (gene/disease/chemical)")
ap.add_argument("inputFile", help = "input files name")
ap.add_argument("outputDirectory", help = "directory of output files")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

userName = args['username']
password = args['password']
pubType = args['pubType'].lower()
inFile = args['inputFile']
outDir = args['outputDirectory']

output = getFileTypeInfo(pubType, outDir) #get tailored info for putator filetype
query = output[0] #query for database
outFile = output[1] #output file name

cnx = dCastDatabase(userName, password)  #get to database
pubSet = getPubSet(cnx, query) #get set of wanted values from database
writeToFile(pubSet, pubType, inFile, outFile) #write data to file

cnx.close() #close connection