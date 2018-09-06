Python scripts to assist with gdancik's CPP repository

################################################
# process new pubtator and mesh files for dcast
################################################

./processFiles - processes pubtator and mesh files in download directory

################################################
# retreive and process pubmed baseline for dcast 
################################################

# retreive pubmed files
python pubmed/pubMedRetrieval.py baseline outputDir email 

# convert from xml to text (for articles in dcast)
python pubmed/write_full_pubmed_to_text.py name password inputDir outputDir 

# stem titles and abstracts
python stem/pmid_and_stem.py inputDirectory outputDirectory 



################################################
# upload PubTator Associations (cd to mysq/)
################################################

loadAssociations dcast.username dcast.password dataDir


################################################
# load cancer-term associations 
################################################

#upload article text from pubmed stemmed *.txt files
Rscript mysql/loadArticleText.R directory [drop]

# lookup patterns in NCI thesaurus
python stem/NCIThesaurusLookUp.py ../misc_data_files/Thesaurus.txt codes.txt cancerterms.txt

# load CancerTerms into DCAST
mysql/loadCancerTerms
