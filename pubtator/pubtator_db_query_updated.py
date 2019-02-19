# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:50:49 2018

@author: kewilliams

Usage:

    python pubtator_db_query_updated.py [-h] username password pubType inputFile outDirectory

Currently handles gene and chemical
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
        query1 = "select GeneID from Genes"
        query2 = "" #only one query to database
        outFile = outDir + "gene2pubtator_updated"
    elif pubType == "chemical":
        query1 = "select distinct(PMID) from PubGene"
        query2 = "select distinct(MeshID) from PharmActionTerms"
        outFile = outDir + "chemical2pubtator_updated"
#    elif pubType == "disease":
#        query1 = ""
#        query2 = ""
#        outFile = outDir + "disease2pubtator_updated"
    else:
        print("Unknown pubtator file type")
        exit()
        
    return outFile, query1, query2
        

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


def getSet(cnx, pubType, query1, query2):
    
    print("Creating set...")    
    cursor = cnx.cursor()
    cursor.execute(query1)
    pubSet1 = {x[0] for x in cursor.fetchall()} #fetches are a single value tuple
    #print(pubSet1)
    print(str(len(pubSet1)) + " items in set")
    
    if pubType == "chemical":
        print("Creating set...")    
        cursor = cnx.cursor()
        cursor.execute(query2)
        pubSet2 = {x[0] for x in cursor.fetchall()} #fetches are a single value tuple
        #print(pubSet2)
        print(str(len(pubSet2)) + " items in set")
    else:
        pubSet2 = {}
    return pubSet1, pubSet2

#genes - pubSet1(GeneID), text2(NCBI_Gene)
#chemical - pubSet1(PMID), pubSet2(MeshID), text1(PMID), text2(MeshID)
def pubTest(pubType, pubSet1, pubSet2, text1, text2):
    
    test = False
    if pubType == "gene":
        if int(text2) in pubSet1:
            test = True
    elif pubType == "chemical":
        if text2 in pubSet2 and int(text1) in pubSet1:
            test = True
#    elif pubType == "disease":
#        something

    return test

def writeToFile(pubSet1, pubSet2, pubType, inFile, outFile):
    
    t1 = timeit.default_timer()
    matchCnt = 0 #counter for number of files written
    lineCnt = 0 #counter to display progress in code
    
    readFile = open(inFile)    
    writeFile = open(outFile, 'w')
    print("Reading pubtator file...")
    writeFile.write(readFile.readline().strip() + '\n')
    
    for line in readFile:
        lineCnt += 1
        if not line.strip() == "": #some lines contained only "" or "\n"
            text = line.split('\t')
            #gene2pubtator - [0] = PMID, [1] = NCBI_Gene, [2] = Mentions, [3] = Resource
            #chemical2pubtator - [0] = PMID, [1] = MeshID, [2] = Mentions, [3] = Resource   
            if pubTest(pubType, pubSet1, pubSet2, text[0], text[1]) == True: #calls function to test validity
                matchCnt += 1
                writeFile.write(line.strip() + '\n')
        
        if lineCnt % 2000000 == 0 and pubType == "gene":
            print(str(lineCnt / 1000000) + " million lines read")
        elif lineCnt %10000000 == 0 and pubType == "chemical":
            print(str(lineCnt / 1000000) + " million lines read")
#        if matchCnt == 100000:
#            print(matchCnt)
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
outFile = output[0] #output file name
query1 = output[1] #query1 for database
query2 = output[2] #query2 for database or ""

cnx = dCastDatabase(userName, password)  #get to database
result = getSet(cnx, pubType, query1, query2) #get set of wanted values from database
pubSet1 = result[0] #set1
pubSet2 = result[1] #set2 - filled or empty depending on file type

writeToFile(pubSet1, pubSet2, pubType, inFile, outFile) #write data to file

cnx.close() #close connection