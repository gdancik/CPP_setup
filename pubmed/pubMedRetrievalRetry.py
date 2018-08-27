#########################################################
# pubmedRetreivalRetry was split off from original 
# pubmedRetreival.py, to redownload *.xml.gz files
# from a directory

# Warning: this has not been tested
#########################################################

import urllib.request
import sys
import os
import glob
import argparse

# Note: consider using pubrunner for this

if len(sys.argv) == 1 or sys.argv[1] != '--retry':
    print("Usage: ")
    print("\tpython", sys.argv[0], "--retry outputDirectory\n")
    print("For additional help, type one of the following:\n\npython pubMedRetrieval.py --retry -h for help")
    sys.exit(1)

ap = argparse.ArgumentParser(description="Redownload PubMed XML files that are in a directory")
ap.add_argument("url", help="ftp url, such as 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' or 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/'")
ap.add_argument("outputDirectory", help = "directory containing files to download again")
ap.prog = ap.prog + " --retry" 
# remove program name and --retry
sys.argv = sys.argv[2:]
# print help if no arguments are provided
if len(sys.argv)== 0:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args(sys.argv))
    
url = args['url']
directory = args['outputDirectory']

if not os.path.exists(directory):
        os.makedirs(directory)

print("Files will be saved to the following directory:", directory)

files = []

files = glob.glob(directory+"/*.xml.gz")
files = [os.path.basename(f) for f in files]

for fileName in files :

  print("retrieving file:", fileName)

  try :
    urllib.request.urlretrieve(url + fileName, directory + "/" + fileName)
  except :
    print("Warning: " + fileName + " could not be downloaded\n")      
