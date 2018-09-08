# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 14:04:39 2018

@author: kewilliams

Date must be formatted M-D-Y.  Year must be four digit year.  I.e. 5-27-2018

Usage:

    python retrieve_pubtator_if_modified.py [-h] outputDirectory email date

"""

import ftputil
from datetime import datetime
import time
import os
import argparse
import sys


def ftpQuery(outDir, email, date):

    date = time.strptime(date, '%m-%d-%Y')
    
    if not outDir.endswith('/'):
        outDir += '/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    
    pubFiles = {"chemical2pubtator.gz", "disease2pubtator.gz", \
                "gene2pubtator.gz", "mutation2pubtator.gz"} #wanted files
        
    host = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous', email)
    path = "pub/lu/PubTator/"
    host.chdir(path)
    
    files = host.listdir('.') #get files from directory
    for file in files:
        if file in pubFiles:
            ts = host.stat(file).st_mtime #get modified date for file
            modifiedDate = datetime.utcfromtimestamp(ts).strftime('%m-%d-%Y') #convert float to date
            modifiedDate = time.strptime(modifiedDate, '%m-%d-%Y') #convert to date with time module
            if date < modifiedDate: #test argument date and modified date
                outFile = outDir + file
                print("retrieving file:", file)
                try :
                    host.download(file, outFile)
                except :
                    print("Warning: " + file + " could not be downloaded\n")  
                


ap = argparse.ArgumentParser(description="Retrieve files if modified after designated date")
ap.add_argument("outputDirectory", help = "directory of output files")
ap.add_argument("email", help = "e-mail requested for FTP access")
ap.add_argument("date", help = "date of previous file retrieval -- format M-D-Y (4 digit year)")

if len(sys.argv)== 0:
    ap.print_help(sys.stderr)
    sys.exit(1)

print(sys.argv)

args = vars(ap.parse_args())

outDir = args['outputDirectory']
email = args['email']
date = args['date']

ftpQuery(outDir, email, date)