##########################################################
# Searches PubArticle Text for patterns form CancerTerms
# and populates PubCancerTerms table
##########################################################

library(RMySQL)

# Connect to the database 'CPP'
con = dbConnect(MySQL(), group = "CPP")


# Create table 'PubCancerTerms'. This table will have two columns:'PMID' and 'TermID'.
if (!dbExistsTable(con,"PubCancerTerms")){
  qry <- paste0("CREATE TABLE PubCancerTerms (
                PMID INT UNSIGNED NOT NULL,
                TermID VARCHAR(20) NOT NULL,
                INDEX index_PMID (PMID),
                INDEX index_TermID(TermID) );")
  dbGetQuery(con, qry)
}  

# Start time to complete this script
t1 <- Sys.time()

# Find number of rows in table 'CancerTerm'.
qry <- paste0("SELECT TermID, Pattern FROM CancerTerms")
res <- dbGetQuery(con, qry)

# This will loop through the rows from the table 'CancerTerm' and extract the words under the 'pattern' column.
for (i in 1:nrow(res)){
 
  TermID <- res$TermID[i]
  pattern <- res$Pattern[i]
  
  # split patterns by "|" and add surrounding quotes, so that phrases are matched exactly
  # (otherwise "a b" will match "a" or "b")
  finalstring <- paste0('"', unlist(strsplit(pattern, "\\|")), '"', collapse = " ")
  cat("(", i, ") Finding PMIDs containing: ", finalstring, , "\n", sep = "")
  
  
  # Inserting the PMIDs of the Articles that contain words or phrase that matches
  # the 'finalstring' and the related 'TermID' from table 'CancerTerm'.
  qry <- paste0("INSERT INTO PubCancerTerms(PMID, TermID)
                SELECT pubarticletext.PMID, '", TermID, "' 
                FROM pubarticletext 
                WHERE MATCH (articleText) AGAINST ('",finalstring,"' IN BOOLEAN MODE);") 
  
  dbGetQuery(con, qry)

}

t2 <- Sys.time()
res <- t2-t1

print(res)

dbDisconnect(con)  
