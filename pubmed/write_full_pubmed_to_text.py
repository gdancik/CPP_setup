# -*- coding: utf-8 -*-
"""
@author kewilliams

Usage:

  write_full_pubmed_to_text.py [-h] username password inputDirectory outputDirectory

Extract dcast article information from PubMed xml files

positional arguments:
  username         dcast username
  password         dcast password
  inputDirectory   directory of input files
  outputDirectory  directory of output files

Tests against dcast database for matching pmids in the PubGene table


simplified sample XML file format (Relevant Data Only):
PubmedArticle
    MedlineCitation
        PMID - text contains PMID
        Article
            Journal
                JournalIssue
                    PubDate
                        Year - text contains PubDate
                        MedlineDate - text contains Year and Month
                Title - text contains Journal Name
            ArticleTitle - Title of Article
            Abstract
                AbstractText - text contains abstract, if multiple tags can contain info
            AuthorList
                Author - findall for authors
                    LastName - text
                    Initials - text
        ChemicalList - Chemical Information
            Chemical
                RegistryNumber
                NameOfSubstance - tag 'UI' has ID / text has name
        MeshHeadingList - Mesh Information
            MeshHeading
                DescriptorName - tag 'UI' has ID / text has name
                QualifierName - tag 'UI' has ID / text has name
    
"""

import shutil #move file location
import timeit
import mysql.connector
from mysql.connector import errorcode
from lxml import etree #slightly faster than xml.etree.ElementTree, also no need to unzip

import sys
import argparse
import glob
import os


#retrieve PMID
def getPmid(medline):
    
    pmid = medline.find('PMID')
    if pmid is not None:
        pmid = pmid.text
    else:
        pmid = ''
    return pmid

#retrieve article title
def getTitle(article):

    title = article.find('ArticleTitle')    
    if title is not None:
        title = title.text
    else:
        title = ''
    return title

#retrieve authors, formatted (Initials + ' ' + LastName  + '; ') for each
def getAuthor(article):
    
    authorList = []
    #no authors needs to be tested from the article branch
    if article.find('AuthorList') is not None:
        authors = article.findall('AuthorList/Author')
        for author in authors:
            initials = author.find('Initials')
            lastName = author.find('LastName')
            if initials is not None and lastName is not None:
                authorString = initials.text + ' ' + lastName.text
            elif lastName is not None:
                authorString = lastName.text 
            elif initials is not None:
                authorString = initials.text
            else:
                authorString = ''
            authorList.append(authorString)
        return '; '.join(authorList)
    else:
        return ''
            
#retrieve journal
def getJournal(journal):

    journal = journal.find('Title')
    if journal is not None:
        journal = journal.text
    else:
        journal = ''
    return journal
        
#retrieve pubDate
def getPubDate(pubDate):
    
    year = pubDate.find('Year')
    
    if year is not None:
        year = year.text
    #if no child Year, child MedlineDate may replace it. Formatted 'Year Month'
    #elif and else case very rare, would harm efficiency to do a .find every time
    elif pubDate.find('MedlineDate') is not None:
        year = pubDate.find('MedlineDate').text.split(' ')[0]
    else:
        year = ''
    return year

#retrieve abstract
def getAbstract(article):
    
    if article.find('Abstract/AbstractText') is not None:
        abstracts = article.findall('Abstract/AbstractText')
        if len(abstracts) == 1: #if one abstract, ignore tags and get text
            abstractText = abstracts[0].text
        elif len(abstracts) > 1:
            abstractText = ''
            #multiple abstracts typically come with hidden headings in tags
            #tags typically have a NlmCategory attribute, if not that then Label attribute
            for abstract in abstracts:
                abText = abstract.text
                if abText is None :
                    abText = ''
                #print("abstract.txt:", abstract.text)
                #print("Nlm:", abstract.attrib.get('NlmCategory','null'))
                #print("Label:", abstract.attrib.get('Label','null'))

                nlm = abstract.attrib.get('NlmCategory')
                if nlm :
                    abstractText += nlm + ' ' + abText + ' ' 
                    continue
                label = abstract.attrib.get('Label')
                if label :
                    abstractText += label + ' ' + abText + ' '
                    continue
                abstractText += abText + ' '
            abstractText = abstractText[:-1] #remove trailing ' '
        else:
            abstractText = ''
    #if Abstract/AbstractText is None, abstract text may be out of place in Abstract child        
    elif article.find('Abstract') is not None:
        abstractText = article.find('Abstract').text
    else:
        abstractText = ''
    return abstractText


#database access for pmids
def dCastDatabase (userName, password, inputDirectory, outputDirectory):
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
    else:
        cursor = cnx.cursor(buffered=True)
        cursor.execute('select distinct pmid from PubGene')
        pmids = set(cursor.fetchall())
        cnx.close()
        pmids = {str(x[0]) for x in pmids}
        print("checking against", len(pmids), "dcast pmids")

        #createTxtFromXMLCheckEach(inputDirectory, cnx)
        #cnx.close()

        createTxtFromXML(inputDirectory, pmids) 


# takes set of pmids and checks each pmid against set
def createTxtFromXML(filePath, pmids):

    #t2 = timeit.default_timer() #begin timer for whole program
    
    errorStr = "" #for try / catch
    
    # get all xml.gz files in specified directory
    files = sorted(glob.glob(filePath +"/*.xml.gz"))
    print("Number of *.xml.gz files found in directory '", filePath, "': ", len(files), sep = "")

    # create outputDirectory if it does not exist
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    errorCount = 0

    for inFile in files:
        t0 = timeit.default_timer()
        
        try:
            pubTree = etree.parse(inFile)
        
        except :            
            if not os.path.exists(outputDirectory + ("/ERRORS/")): #create folder for failed file
                os.makedirs(outputDirectory + ("/ERRORS/"))
            shutil.copy(inFile, outputDirectory + "/ERRORS/" + os.path.basename(inFile)) #move to ERROR folder
            errorStr = os.path.basename(inFile) + " - " + str(sys.exc_info()[0])
            print(errorStr)
            f = open(outputDirectory + "/ERRORS/log.txt", "a")
            f.write(errorStr + "\n")
            f.close()
            errorCount += 1
            continue #skip to next file
        
             
        outFile = outputDirectory + "/extracted_" + os.path.basename(inFile).replace(".xml.gz", ".txt")
        
        writeFile = open(outFile, 'w') #open file for data transfer
        
        for pubmedArticle in pubTree.getiterator('PubmedArticle'):
            if getPmid(pubmedArticle.find('MedlineCitation')) in pmids :
                writeToFile(pubmedArticle, writeFile)
            pubmedArticle.clear() #clearing nodes slightly increases speed
        t1 = timeit.default_timer()
        print("Successful Write : " + outFile + " : " + str(t1 - t0))   
    
    #t3 = timeit.default_timer() #end time for whole program
    #print("\nTotal time of execution: " + str(t3 - t2))
    if errorCount is not 0 :
        print("\nWarning:", errorCount, "files could not written. See", outputDirectory + "/ERRORS/log.txt for more information")
        

# takes db connection 'cnx' and checks each pmid one at a time by querying db
def createTxtFromXMLCheckEach(filePath, cnx):

    #t2 = timeit.default_timer() #begin timer for whole program
    
    query = ("select PMID from PubGene where PMID = ") #generic query
    errorStr = "" #for try / catch
    
    # get all xml.gz files in specified directory
    files = sorted(glob.glob(filePath +"/*.xml.gz"))
    print("Number of *.xml.gz files found in directory '", filePath, "': ", len(files), sep = "")

    # create outputDirectory if it does not exist
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    errorCount = 0

    for inFile in files:
        t0 = timeit.default_timer()
        
        try:
            pubTree = etree.parse(inFile)
        
        except :            
            if not os.path.exists(outputDirectory + ("/ERRORS/")): #create folder for failed file
                os.makedirs(outputDirectory + ("/ERRORS/"))
            shutil.copy(inFile, outputDirectory + "/ERRORS/" + os.path.basename(inFile)) #move to ERROR folder
            errorStr = os.path.basename(inFile) + " - " + str(sys.exc_info()[0])
            print(errorStr)
            f = open(outputDirectory + "/ERRORS/log.txt", "a")
            f.write(errorStr + "\n")
            f.close()
            errorCount += 1
            continue #skip to next file
        
             
        outFile = outputDirectory + "/extracted_" + os.path.basename(inFile).replace(".xml.gz", ".txt")
        
        writeFile = open(outFile, 'w') #open file for data transfer
        
        #unbuffered fetchone() causes error after a large amount of queries, reusing a cursor
        #repeatedly without fetching all results leads to "unread result found"
        #buffered allows all results to be fetched, but only returns one to code
        cursor = cnx.cursor(buffered=True)
        
        for pubmedArticle in pubTree.getiterator('PubmedArticle'):
            cursor.execute(query + getPmid(pubmedArticle.find('MedlineCitation')))
            row = cursor.fetchone()
            if row != None:
                writeToFile(pubmedArticle, writeFile)
            pubmedArticle.clear() #clearing nodes slightly increases speed
        cursor.close()
        t1 = timeit.default_timer()
        print("Successful Write : " + outFile + " : " + str(t1 - t0))   
    
    #t3 = timeit.default_timer() #end time for whole program
    #print("\nTotal time of execution: " + str(t3 - t2))
    if errorCount is not 0 :
        print("\nWarning:", errorCount, "files could not written. See", outputDirectory + "/ERRORS/log.txt for more information")
        


def writeToFile (pubmedArticle, writeFile):
    
    #multiple calls from same child node instead of starting from root
    medline = pubmedArticle.find('MedlineCitation')
    pmid = getPmid(medline)
    article = medline.find('Article')
    title = getTitle(article)
    author = '' #getAuthor(article)
    abstract = getAbstract(article)
    journal = '' #article.find('Journal')
    journalTitle = '' #getJournal(journal)
    pubDate = '' # journal.find('JournalIssue/PubDate')
    date = '' #getPubDate(pubDate)
  
    # make sure not to output None because that causes problems in pmid_and_stem.py 
    if title is None :
        title = ''
    if abstract is None :
        abstract = ''

    writeFile.write(ascii(pmid) + '\t' + ascii(title) + '\t' + ascii(author) + '\t' +
                    ascii(journalTitle) + '\t' + ascii(date) + '\t' + ascii(abstract) + '\n')
    

# main program
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Extract dcast article information from PubMed xml files')
ap.add_argument("username", help="dcast username")
ap.add_argument("password", help="dcast password")
ap.add_argument("inputDirectory", help = "directory of input files")
ap.add_argument("outputDirectory", help = "directory of output files")

# print help if no arguments are provided
if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())

userName = args['username']
password = args['password']

inputDirectory = args['inputDirectory']
outputDirectory = args['outputDirectory']

dCastDatabase(userName, password, inputDirectory, outputDirectory)
