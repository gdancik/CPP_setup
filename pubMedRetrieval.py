#########################################################
# Downloads 2018 PubMed baseline data, which includes
#     pubmed18n0001.xml.gz - pubmed18n0929.xml.gz
#########################################################

import urllib.request
import sys
import os
import glob

if len(sys.argv) != 2 and len(sys.argv) != 3 :

    msg = "Usage: python pubMedRetrieval directory [--retry]\n Note: use --retry only to re-download all files in the directory" 
    raise Exception(msg)

directory = sys.argv[1]
retry = sys.argv[2] == "--retry"


if not os.path.exists(directory):
        os.makedirs(directory)

print("Files will be saved to the following directory:", directory)

url = "ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"

#numStop = 5   # use for testing

files = []

if retry :
    files = glob.glob(directory+"/*.xml.gz")
    files = [os.path.basename(f) for f in files]
else :
    numStop = 929 # use to get all abstracts
    #fileNumStr = str(fileNum)
    #fileNumStr = fileNumStr.rjust(4, "0")  # pad string with 0s
    #fileName = "pubmed18n" + fileNumStr + ".xml.gz"
    files = ["pubmed18n" + str(fileNum).rjust(4, "0") + ".xml.gz" for fileNum in range(1,numStop)]


for fileName in files :

  if not retry and os.path.exists(directory + "/" + fileName) :
      print("File already exists and will not be downloaded: " + fileName)
      continue

  print("retrieving file:", fileName)

  try :
    urllib.request.urlretrieve(url + fileName, directory + "/" + fileName)
  except :
    print("Warning: " + fileName + " could not be downloaded\n")      
