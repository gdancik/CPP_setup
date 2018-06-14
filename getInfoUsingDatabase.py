import pubmed_parser as pp
import mysql.connector
from mysql.connector import errorcode


#database access for pmids
def pmidsDatabase (pubmed_dict, file):
    try:
        #best effort to conceal password, ugly but works
        #text file contains password without '' or "" encapsulation
        #only str() made the argument valid
        inFile = open("pmidDatabaseInfo.txt")
        dataPass = inFile.readline()
        inFile.close()
        cnx = mysql.connector.connect(user='root', password=str(dataPass),
                                      database='summerbio')
    except mysql.connector.Error as err:
        
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        writeFile = open(file, 'w')
        cursor = cnx.cursor()
        query = ("SELECT pmids FROM pmids WHERE pmids = ") #generic query for loop
        for item in pubmed_dict:
            cursor.execute(query + item['pmid']) #query + current items pmid
            row = cursor.fetchone() #fetches result of query, either None or matching value
            if row != None : #if matching value found
                writeToFile(item, writeFile) #write item in pubmed_dict to file

        writeFile.close()
        cursor.close()
        cnx.close()

#write pmid matches to file with desired information
def writeToFile (item, writeFile):
    writeFile.write(item['pmid'] + '\t' + item['title'] + '\t' + 
                    item['author'] + '\t' + item['journal'] + '\t' +
                    item['pubdate'] + '\t' + item['abstract'] + '\n')
    
#parse xml into dictionary
def createPubDict (file):
    pubmed_dict = pp.parse_medline_xml(file)
    return pubmed_dict

pubFile = "pubmedsample18n0001.xml"
matchOutFile = "pmidMatchFromDatabase.txt"

pubmed_dict = createPubDict(pubFile)
pmidsDatabase(pubmed_dict, matchOutFile)