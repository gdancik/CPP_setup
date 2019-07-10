#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 10:25:53 2018
Processes disease2pubtator file by
    (1) keeping only cancer related PMIDs
    (2) removing redundant Mesh IDs
    (3) keeping only human genes

@author: dancikg
"""

from collections import defaultdict

import argparse, sys

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Clean Pubtator Disease data to include only cancer-related articles with human genes and remove redundant Mesh IDs')
ap.add_argument("meshTree", help = "MeshTreeHierarchyWithScopeNotes.txt file")
ap.add_argument("diseaseFile", help = "disease2pubtator file")
ap.add_argument("geneFile", help = "gene2pubtator_processed file")
ap.add_argument("outputFile", help = "output filepath and name")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

meshTree = args['meshTree']
diseaseFile = args['diseaseFile']
geneFile = args['geneFile']
outFile = args['outputFile']

print("Reading", meshTree, "...")

meshDictionary = defaultdict(list)
# retrieve cancer related articles
for line in open(meshTree):
    data = line.strip().split('\t')
    if data[0].startswith('C04'):
        meshDictionary[data[1]].append(data[0])

cancerMeshIDs = meshDictionary.keys()


print("Reading", diseaseFile, "...")
# open file
f = open(diseaseFile)

rows = [r.replace("MESH:","") for r in f]

# keep rows that are cancer-related
rows = map(lambda x: x.split('\t'), 
           filter(lambda x: x.split()[1] in cancerMeshIDs, rows)
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


print("Reading", geneFile, "...")
#get set of pmids for human genes
genePMID = {line.split('\t')[0] for line in open(geneFile)}

print("filtering human genes...")
humanCancerPmidDict = {}
#create dictionary of pmids that are cancer related with human genes
for key in pmidDictionary:
    if str(key) in genePMID:
        humanCancerPmidDict[key] = pmidDictionary[key]


print("Writing to file...")
fout = open(outFile, "w")
fout.write("PMID\tMeshID\n")
for pmid, mesh in humanCancerPmidDict.items() :    
    a = "\n".join([pmid + '\t' + x for x in mesh])
    fout.write(a+'\n')

print("Results output to:", outFile)