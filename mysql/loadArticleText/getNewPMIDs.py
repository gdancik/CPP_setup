# -*- coding: utf-8 -*-
"""
@author gdancik 

Usage:

  getNewPMIDs.py [-h] username password pmids.txt new.txt 

Output to a file PMIDS in pmids.txt that are not in dcast.PubGene

positional arguments:
  username         dcast username
  password         dcast password
  pmids.txt        file containing pmids (from cpp-output-pmids) 
  new.txt          output file to contain the new pmids
"""

import mysql.connector
from mysql.connector import errorcode

import sys
import argparse

#database access for pmids (modified from kewilliams)
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
    else : 

        query = "select distinct PMID from PubGene" 
        cursor = cnx.cursor(buffered=True)
        cursor.execute(query) 
        pmids = cursor.fetchall() 
        pmids = {str(i[0]) for i in pmids}
        cnx.close()
        return pmids
            
    
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Extract dcast article information from PubMed xml files')
ap.add_argument("username", help="dcast username")
ap.add_argument("password", help="dcast password")
ap.add_argument("pmids", help = "file containing pmids")
ap.add_argument("outFile", help = "output file")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

userName = args['username']
password = args['password']
pmids = args['pmids']
outFile = args['outFile']


print("reading old pmids...")
f = open(pmids)
f.readline()
old = {i.strip() for i in f}
f.close()

print("reading current pmids from dcast...")
curr = dCastDatabase(userName, password)

# find new pmids
d = curr - old

print("# of old pmids: ", len(old))
print("# of current pmids: ", len(curr))
print("# of new pmids: ", len(d))
print()

f = open(outFile, "w")
print("outputting pmids to file: ", outFile)
for i in d :
    f.write(str(i) + '\n')
      
      







