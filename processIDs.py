"""
Processes pubtator files ensuring each line has only one ID; multiple lines
are created for rows having multiple IDs separated by a comma or semi-colon

positional arguments:
  inputFile   the input file, which is tab delimited
  index       the index of the column to check, starting at 0
  outputFile  the output file
"""

# For example, 
#               col1    A,B     col3   
#   
# becomes       col1    A       col3
#               col1    B       col3    

import argparse
import re
import sys

# processes the file
def processMulti(file, index, outfile) :
    fin = open(file)
    f = open(outfile, "w")
    for r in fin :
        s = splitRow(r.strip(),index)
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
    return row + '\n'
  rows = [replace(x,index,i) for i in ids]
  ans = '\n'.join(['\t'.join(i) for i in rows])
  return ans + '\n'


# creates and returns a new list with x[index] = val
def replace(x, index, val) :
  xx = list(x)
  xx[index] = val
  return xx

# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Processes pubtator files ensuring each line has only one ID; multiple lines are created for rows having multiple IDs separated by a comma or semi-colon')
ap.add_argument("inputFile", help = "the input file, which is tab delimited")
ap.add_argument("index", help = "the index of the column to check, starting at 0", type = int)
ap.add_argument("outputFile", help = "the output file")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

inFile = args['inputFile']
index = args['index']
outFile = args['outputFile']

print("processing file", inFile, "...")
processMulti(inFile, index, outFile)
print("results output to:", outFile)
