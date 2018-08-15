#########################################################
# Downloads 2018 PubMed baseline data, which includes
#     pubmed18n0001.xml.gz - pubmed18n0929.xml.gz
#########################################################

import urllib.request
import sys
import os
import glob
import argparse


if len(sys.argv) == 1 or sys.argv[1] != '--by-num' and sys.argv[1] != '--retry':
    print("Usage: ")
    print("\tpython", sys.argv[0], "--by-num url startNum endNum outputDirectory")
    print("\tpython", sys.argv[0], "--retry outputDirectory\n")
    print("For additional help, type one of the following:\n\npython --by-num -h\npython --retry -h for help")
    sys.exit(1)

if sys.argv[1] == '--by-num' :
    ap = argparse.ArgumentParser(description="Retrieve PubMed XML files from 'startNum' to 'endNum'\nNote: a file will not be downloaded if it already exists")
    ap.add_argument("url", help="ftp url, such as 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/' or 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/'")
    ap.add_argument("startNum", type = int, help="starting file number")
    ap.add_argument("endNum", type = int, help="ending file number")
    ap.add_argument("outputDirectory", help = "directory of output files")
    ap.prog = ap.prog + " --by-num" 

    # remove program name and --by-num
    sys.argv = sys.argv[2:]
    # print help if no arguments are provided
    if len(sys.argv)== 0:
        ap.print_help(sys.stderr)
        sys.exit(1)

    args = vars(ap.parse_args(sys.argv))
    startNum = args['startNum']
    endNum = args['endNum']
    retry = False
else :
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
    retry = True
    
    
url = args['url']
directory = args['outputDirectory']


if not os.path.exists(directory):
        os.makedirs(directory)

print("Files will be saved to the following directory:", directory)

files = []

if retry :
    files = glob.glob(directory+"/*.xml.gz")
    files = [os.path.basename(f) for f in files]
else :
    files = ["pubmed18n" + str(fileNum).rjust(4, "0") + ".xml.gz" for fileNum in range(startNum,endNum+1)]


for fileName in files :

  if not retry and os.path.exists(directory + "/" + fileName) :
      print("File already exists and will not be downloaded: " + fileName)
      continue

  print("retrieving file:", fileName)

  try :
    urllib.request.urlretrieve(url + fileName, directory + "/" + fileName)
  except :
    print("Warning: " + fileName + " could not be downloaded\n")      
