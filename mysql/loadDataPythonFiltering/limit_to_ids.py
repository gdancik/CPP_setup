# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:50:49 2018

@author: gdancik

Usage:

    python limit_to_ids.py [-h] username password inputFile outDirectory

"""

import mysql.connector
from mysql.connector import errorcode
import os
import sys
import argparse
import timeit
      
def getDistinctPMIDs(userName, password) :
    cnx = None
    try: 
        cnx = mysql.connector.connect(user=userName, password=password, database='dcast')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            exit()
        else:
            print(err)
            exit()
    cursor = cnx.cursor()
    query = "select distinct PMID from PubGene"
    print("Retreiving distinct PMIDs....")
    cursor.execute(query)
    pmids = {x[0] for x in cursor.fetchall()} #fetches are a single value tuple
    cnx.close() #close connection
    return pmids

def getDistinctIDsFromFile(id_file, id_delim) :
    with open(id_file) as f :
        f.readline()
        s = { int(x.split(id_delim)[0].strip()) for x in f }
        return s


desc = '''Filter out IDs, based on PubGene table or id-file. If dcast info is specified, filter is done using PMIDs in PubGene. 
          Otherwise IDs are obtained from first column of id-file. It is assumed that all files have a header.'''

ap = argparse.ArgumentParser(description=desc)
ap.add_argument("input", help = "input files name")
ap.add_argument("idx", help = "column index (starting at 0) of input file containing IDs to filter by")
ap.add_argument("output", help = "output file name")
ap.add_argument("--username", help="dcast username")
ap.add_argument("--password", help="dcast password")
ap.add_argument("--delim", help="input file delimiter", default = "\t")
ap.add_argument("--id-file", help="file containing ids in first column")
ap.add_argument("--id-delim", help="delimiter for id-file")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

userName = args['username']
password = args['password']
inFile = args['input']
idx = int(args['idx'])
outFile = args['output']
delim = args['delim']
id_file = args['id_file']
id_delim = args['id_delim']


if [id_file,password].count(None) == 2 :
    print("You must specify dcast username/password or id-file/id-delim")
    sys.exit(1)

if [id_file, id_delim].count(None) == 1 :
    print("To use id-file, you must specify both --id-file and --id-delim")
    sys.exit(1)

with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
    None

ids = None
if id_file != None :
    print("Getting IDs from file: ", id_file)
    ids = getDistinctIDsFromFile(id_file, id_delim)
else :
    print("Getting PMIDs from PubGene...")
    ids = getDistinctPMIDs(userName, password)

print("Filtering based on", len(ids), "ids...")

with open(inFile, 'r') as fin, open(outFile, 'w') as fout:
    fout.write(fin.readline())
    count = 0
    total = 0
    for line in fin :
        if line.strip() == '' :
            continue
        total += 1
        if int(line.split(delim)[idx]) in ids :
            fout.write(line)
        else :
            count += 1

print("Total number of records:", total)
print("Number of records filtered out:", count)
