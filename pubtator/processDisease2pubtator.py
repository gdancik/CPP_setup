#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 10:25:53 2018
Processes disease2pubtator file by
    (1) keeping only cancer related PMIDs
    (2) removing redundant Mesh IDs

@author: dancikg
"""

import mysql.connector
from mysql.connector import errorcode

from collections import defaultdict

import argparse, sys

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Clean Pubtator Disease data to include only cancer-related articles and remove redundant Mesh IDs')
ap.add_argument("username", help = "dcast username")
ap.add_argument("password", help = "dcast password")
ap.add_argument("inputFile", help = "disease2pubtator file")
ap.add_argument("outputFile", help = "output filepath and name")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

userName = args['username']
password = args['password']
file = args['inputFile']
outFile = args['outputFile']


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
    raise
    
cursor = cnx.cursor()

# create a set of cancerMeshIDs
query = """select MeshID, TreeID from MeshTerms where            
           MeshTerms.TreeID like "C04.%" or 
           MeshTerms.TreeID = "C04"; 
           """

print("Getting Cancer Mesh Info...")
cursor.execute(query)
res = cursor.fetchall()

meshDictionary = defaultdict(list)
for k, v in res:
    meshDictionary[k].append(v)


cancerMeshIDs = meshDictionary.keys()


print("Reading", file, "...")
# open file
f = open(file)

# keep rows that are cancer-related
rows = map(lambda x: x.split('\t'), 
           filter(lambda x: x.split()[1] in cancerMeshIDs, f)
       )


# create dictionary of pmid: meshID associations
pmidDictionary = defaultdict(set)
for r in rows:
    pmid = r[0]
    mesh = r[1]
    pmidDictionary[pmid].add(mesh)


def inList(s,l) :
    """ returns true if string s is in any element of list l """
    return len([1 for i in l if s in i]) > 0
    
def anyOverlap(a, b) :
    """ returns True if two sets overlap """
    return len( a & b ) > 0
    

def removeRedundantMesh(meshIDs) :
    """ returns updated meshID list with redundant meshIDs removed """
    
    # get corresponding treeIDs
    trees = []
    for m in meshIDs :
        trees += meshDictionary[m]
    
    trees = list(set(trees))

    # which ones do we keep?
    allTrees = trees[:]
    keepTrees = []
    n = len(trees)
    for i in range(n):
        t = trees[i]
        trees.remove(t)
    
        if not inList(t, trees):
            keepTrees += [t]
            
        trees = allTrees[:]

    keepTrees = set(keepTrees)

    mesh = [m for m in meshIDs 
            if anyOverlap(set(meshDictionary[m]), keepTrees)]

   # l = [(m,meshDictionary[m]) for m in meshIDs]
   # print("original:")
   # [print(x) for x in l]
   # print("keeping:", mesh)
    return mesh


# update pmid mesh associations
print("updating pmid-mesh associations...")
for k,v in pmidDictionary.items() :
    pmidDictionary[k] = removeRedundantMesh(pmidDictionary[k])

print("Writing to file...")
fout = open(outFile, "w")
fout.write("PMID\tMeshID\n")
for pmid, mesh in pmidDictionary.items() :    
    a = "\n".join([pmid + '\t' + x for x in mesh])
    fout.write(a+'\n')

print("Results output to:", outFile)

    
    
    
     