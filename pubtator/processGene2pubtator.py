"""
@author: dancikg

Processes pubtator files ensuring each line has only one ID; multiple lines
are created for rows having multiple IDs separated by a comma or semi-colon
Genes not in geneFile are removed

positional arguments:
  inputFile   the input file, which is tab delimited
  outputFile  the output file
  geneFile    csv file containing valid geneIDs in 1st column
"""

# For example, 
#               col1    A,B     col3   
#   
# becomes       col1    A       col3
#               col1    B       col3    

import argparse
import re
import sys
from col_to_set import col_to_set

indexGeneID = 1

# processes the file
def processMulti(file,outfile, geneFile) :
    genes = col_to_set(geneFile, ',', 0)
    print("# valid genes:", len(genes))
    #print('Genes:', list(genes)[:5])

    fin = open(file)
    f = open(outfile, "w")
    for row in fin :
        #print(row)
        r = row.split()
        #print(r[index])
        #input('Enter to continue...')
        #print()
        if r[indexGeneID] in genes :
            s = splitRow(row,indexGeneID)
            f.write(s)

# splits row into multiple rows
# changes, eg. col1\t A,B,C \t col3, ...
# to           col1\t A     \t col3, ...
#              col1\t B     \t col3, ...
#              col1\t C     \t col3, ...
def splitRow(row, index) :
  x = row.split("\t")
  ids = re.split(",|;",x[index])
  if len(ids) == 1 :
    return row.strip() + '\n'
  rows = [replace(x,index,i) for i in ids]
  ans = '\n'.join(['\t'.join(i) for i in rows])
  return ans.strip() + '\n' 


# creates and returns a new list with x[index] = val
def replace(x, index, val) :
  xx = list(x)
  xx[index] = val
  return xx

# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Processes pubtator files ensuring each line has only one ID; multiple lines are created for rows having multiple IDs separated by a comma or semi-colon')
ap.add_argument("inputFile", help = "the input file, which is tab delimited")
ap.add_argument("outputFile", help = "the output file")
ap.add_argument("geneFile", help = "csv file containing valid geneIDs in 1st column")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

inFile = args['inputFile']
outFile = args['outputFile']
geneFile = args['geneFile']

print("processing file", inFile, "...")
processMulti(inFile, outFile, geneFile)
print("results output to:", outFile)
