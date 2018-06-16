# -*- coding: utf-8 -*-
"""
At the bottom of the code before the execution of createTxtFromXML function,
adjust the filePath variable accordingly, code should execute without any
other alterations.

Test against dcast database for matching pmids in the PubGene table

numStop is the total number of files + 1, currently 928 files, this may need
to be updated as additional pubmed updates may change the number of files

"""
import pubmed_parser as pp
#import timeit
import mysql.connector
from mysql.connector import errorcode

#parse xml into dictionary
def createPubDict (file):
    pubmed_dict = pp.parse_medline_xml(file)
    return pubmed_dict

#database access for pmids
def dCastDatabase (filePath):
    try:
        #best effort to conceal password, ugly but works
        #text file contains password without '' or "" encapsulation
        inFile = open("databaseInfo.txt")
        dataPass = inFile.readline()
        inFile.close()
        cnx = mysql.connector.connect(user='root', password=str(dataPass),
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
        createTxtFromXML(filePath, cnx)
        cnx.close()

def createTxtFromXML(filePath, cnx):    

    query = ("select PMID from PubGene where PMID = ") #generic query
    numStop = 929 # use to get all abstracts: Currently 928
    numStop = 5   # use for testing
    
    for fileNum in range(1, numStop):
#        t0 = timeit.default_timer()
        fileNumStr = str(fileNum)
        fileNumStr = fileNumStr.rjust(4, "0")  # pad string with 0s
    
        inFile = filePath + "pubmed18n" + fileNumStr + ".xml.gz" #read xml file       
        outFile = filePath + "extracted_pubmed18n" + fileNumStr + ".txt" #write text file
        
        writeFile = open(outFile, 'w') #open file for data transfer
        
        print("reading file:", "pubmed18n" + fileNumStr + ".xml.gz")
        
        #create dictionary from retrieved xml.gz
        pubmed_dict = createPubDict(inFile)
        
        print("writing file:", "extracted_pubmed18n" + fileNumStr + ".txt") #show progress in execution
        
        #unbuffered fetchone() causes error after a large amount of queries, reusing a cursor
        #repeatedly without fetching all results leads to "unread result found"
        #buffered allows all results to be fetched, but only returns one to code
        cursor = cnx.cursor(buffered=True)
        
        for item in pubmed_dict:
            cursor.execute(query + item['pmid']) #query + current items pmid
            row = cursor.fetchone() #fetches result of query, either None or matching value
            if row != None : #if matching value found
                 writeToFile(item, writeFile) #write item in pubmed_dict to file
        writeFile.close() #next iteration will be new file name, this file is no longer used
        cursor.close()
#        t1 = timeit.default_timer()
#        print(t1 - t0)

def writeToFile (item, writeFile):

    writeFile.write(ascii(item['pmid']) + '\t' + 
                    ascii(item['title']) + '\t' + 
                    ascii(item['author']) + '\t' + 
                    ascii(item['journal']) + '\t' +
                    ascii(item['pubdate']) + '\t' + 
                    ascii(item['abstract']) + '\n')
    

#path for xml and text files, only necessary change for user
filePath = "C:/Users/kewil/PubMedXML/"
dCastDatabase(filePath)
