from operator import itemgetter
import pubmed_parser as pp

#parse xml into dictionary
def createPubDict (file):
    pubmed_dict = pp.parse_medline_xml(file)
    return pubmed_dict

#create sorted list of pmid values from text file
def createPmidList (file):
    pmid = [line.strip() for line in open(file)]
    pmid.sort()
    return pmid

#both dictionary and pmid list are sorted, single pass through dictionary to
#match the requested pmid articles.  write matching data to file
def printPmidListMatches(pubmed_dict, pmidList, file):
    pubmed_dict = sorted(pubmed_dict, key = itemgetter('pmid')) #sort dict by pmid
    outFile = open(file, 'w')
    index = 0 #start at beginning of pmid list
    for item in pubmed_dict: #increment through pmid keys in the dictionary
        if item['pmid'] == pmidList[index]: #if key in list
            outFile.write(item['title'] + '\t' + item['abstract'] + '\t' +
                          item['journal'] + '\t' + item['author'] + '\t' +
                          item['pubdate'] + '\n')
            index += 1 #next pmid in text file
            if index >= len(pmidList): #break if at end of list
                break
    outFile.close()
    
# alternate way with sets
def createPmidSet (file):
    pmid = [line.strip() for line in open(file)]
    pmidSet = set(pmid)
    return pmidSet

def printPmidSetMatches(pubmed_dict, pmidSet, file):
    outFile = open(file, 'w')
    index = 0 #start at beginning of pmid list
    for item in pubmed_dict: #increment through pmid keys in the dictionary
        if item['pmid'] in pmidSet: #if key in set
            outFile.write(item['title'] + '\t' + item['abstract'] + '\t' +
                          item['journal'] + '\t' + item['author'] + '\t' +
                          item['pubdate'] + '\n')
            index += 1 #next pmid in text file
            if index >= len(pmidSet): #break if at end of list
                break
    outFile.close()
                

pubFile = "pubmedsample18n0001.xml"
pmidFile = "pmids.txt"
matchOutFile = "pmidMatchData.txt"

pubmed_dict = createPubDict(pubFile)

pmidList = createPmidList(pmidFile)
printPmidListMatches(pubmed_dict, pmidList, matchOutFile)

#pmidSet = createPmidSet(pmidFile)
#printPmidSetMatches(pubmed_dict, pmidSet, matchOutFile)
