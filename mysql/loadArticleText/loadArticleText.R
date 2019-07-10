# Upload multiple text files into database table

cargs <- commandArgs(TRUE)
if (length(cargs) <1 | length(cargs) > 2) {
  cat("Usage: Rscript loadArticleText.R directory [drop]\n")
  cat("\tdirectory - directory containing pubmed txt files\n")
  cat("\tdrop - optional, will drop PubArticleText if specified\n")
  stop()
}

library(RMySQL)

drop <- "none"
# Path to data files
if (length(cargs) == 2) {
    drop = cargs[2]
    if (drop != "drop") {
        stop("Invalid second argument. If specified, second argument must be 'drop'")
    }
}

path = cargs[1]
file.names <- dir(path, pattern = ".txt")

# connect to the database CPP
con = dbConnect(MySQL(), group = "CPP")

if (drop == "drop") {
  qry <- paste0("DROP TABLE PubArticleText")
  dbGetQuery(con, qry)
} 

# Create table PubArticleText if it does not exist
if (!dbExistsTable(con,"PubArticleText")){
  qry <- paste0("CREATE TABLE PubArticleText (
                PMID INT UNSIGNED NOT NULL,
                articleText text,
                FULLTEXT (articleText));")
  dbGetQuery(con, qry)
}  

# Loop through the files in folder to load data into table PubArticleText
for (i in 1:length(file.names)) {
  print(paste0("Loading articles from: ", file.names[i]))

  qry <- paste0("LOAD DATA LOCAL INFILE '",path, "/" ,file.names[i],"' INTO TABLE PubArticleText 
                 Fields enclosed by '''' LINES TERMINATED BY '\n'")
  dbGetQuery(con, qry)
}

dbDisconnect(con)  
