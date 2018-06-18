#########################################################
# Downloads 2018 PubMed baseline data, which includes
#     pubmed18n0001.xml.gz - pubmed18n0929.xml.gz
#########################################################

import urllib.request
import sys
import os

if len(sys.argv) != 2 :

    msg = "Usage: python pubMedRetrieval directory" 
    raise Exception(msg)

directory = sys.argv[1]

if not os.path.exists(directory):
        os.makedirs(directory)

print("Files will be saved to the following directory:", directory)

url = "ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"

numStop = 930 # use to get all abstracts
numStop = 5   # use for testing

for fileNum in range(1, numStop) :
  fileNumStr = str(fileNum)
  fileNumStr = fileNumStr.rjust(4, "0")  # pad string with 0s

  fileName = "pubmed18n" + fileNumStr + ".xml.gz"
  print("retrieving file:", fileName)

  urllib.request.urlretrieve(url + fileName, directory + "/" + fileName)

