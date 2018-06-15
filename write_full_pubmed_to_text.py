# -*- coding: utf-8 -*-
"""
At the bottom of the code before the execution of createTxtFromXML function,
adjust the filePath variable accordingly, code should execute without any
other alterations.  

ascii() adds '' to each string, using [1:-1] removes this but adds time
timeit is commented out but it was useful to determine whether removing 
characters before writing to file was too time consuming.
timeit.default_timer() should work across platforms.

numStop is the total number of files + 1, currently 928 files, this may need
to be updated as additional pubmed updates may change the number of files

"""
import pubmed_parser as pp
#import timeit

#parse xml into dictionary
def createPubDict (file):
    pubmed_dict = pp.parse_medline_xml(file)
    return pubmed_dict

def createTxtFromXML(filePath):    


    numStop = 929 # use to get all abstracts: Currently 928
    numStop = 5   # use for testing
    
    for fileNum in range(1, numStop):
#        t0 = timeit.default_timer()
        fileNumStr = str(fileNum)
        fileNumStr = fileNumStr.rjust(4, "0")  # pad string with 0s
    
        inFile = filePath + "pubmed18n" + fileNumStr + ".xml.gz" #read xml file       
        outFile = filePath + "extracted_pubmed18n" + fileNumStr + ".txt" #write text file
        
        writeFile = open(outFile, 'w') #open file for data transfer
        
        #create dictionary from retrieved xml.gz
        pubmed_dict = createPubDict(inFile)
        print("writing file:", "extracted_pubmed18n" + fileNumStr) #show progress in execution
        for item in pubmed_dict:
            writeToFile(item, writeFile) #write desired info to file
            
        writeFile.close() #next iteration will be new file name, this file is no longer used
#        t1 = timeit.default_timer()
#        print(t1 - t0)

def writeToFile (item, writeFile):
    #write file removing '' encapsulation from ascii()
    writeFile.write(ascii(item['pmid'])[1:-1] + '\t' + 
                    ascii(item['title'])[1:-1] + '\t' + 
                    ascii(item['author'])[1:-1] + '\t' + 
                    ascii(item['journal'])[1:-1] + '\t' +
                    ascii(item['pubdate'])[1:-1] + '\t' + 
                    ascii(item['abstract'])[1:-1] + '\n')
    #write file ignoring '' encapsulation from ascii()
#    writeFile.write(ascii(item['pmid']) + '\t' + 
#                    ascii(item['title']) + '\t' + 
#                    ascii(item['author']) + '\t' + 
#                    ascii(item['journal']) + '\t' +
#                    ascii(item['pubdate']) + '\t' + 
#                    ascii(item['abstract']) + '\n')
    

#path for xml and text files, only necessary change for user
filePath = "C:/Users/kewil/PubMedXML/"
createTxtFromXML(filePath)
