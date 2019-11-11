Python scripts to assist with gdancik's CPP repository

######################################################
# (1) process new pubtator and mesh files for dcast
#       Required with DB creation: yes
#       Required with DB updates: yes
######################################################

./processFiles - processes pubtator and mesh files in download directory

#############################################################
# (2) retreive and process pubmed baseline for dcast
#       Required with DB creation: yes
#       Required with DB updates: no
#############################################################

# retreive pubmed files
python pubmed/pubMedRetrieval.py baseline outputDir email 

# convert from xml to text (for articles in dcast)
python pubmed/write_full_pubmed_to_text.py name password inputDir outputDir 

# stem titles and abstracts
python stem/pmid_and_stem.py inputDirectory outputDirectory 



##############################################################
# (3) upload PubTator Associations (cd to mysq/)
#       Required with DB creation: yes
#       Required with DB updates: yes
##############################################################

loadAssociations dcast.username dcast.password dataDir

##############################################################
# (4) load cancer-term associations 
#       Required with DB creation: yes
#       Required with DB updates: no 
##############################################################

#upload article text from pubmed stemmed *.txt files
Rscript mysql/loadArticleText.R directory [drop]

# populate cancer term associations
Rscript loadArticleText/findCancerTermAssociations.R 

# lookup patterns in NCI thesaurus
python stem/NCIThesaurusLookUp.py ../misc_data_files/Thesaurus.txt codes.txt cancerterms.txt

# load CancerTerms into DCAST
mysql/loadCancerTerms

#########################################################################
# (4) Identify new PMIDs (these would not have cancer-term associations) 
#       Required with DB creation: no 
#       Required with DB updates: yes
#########################################################################

# creates file called missing.txt with new pmids
pubmed/getMissingPMIDS 

# retreive PMIDs from PubMed in batches of 500, save to missingPMIDs directory
python pubmed/entrez_pubmed_retrieve.py missing.txt missingPMIDS dancikg@easternct.edu

# stem files
python stem/pmid_and_stem.py missingPMIDS/ missingPMIDSstemmed

# load articles 
Rscript loadArticleText.R ../../missingPMIDSstemmed/ drop
