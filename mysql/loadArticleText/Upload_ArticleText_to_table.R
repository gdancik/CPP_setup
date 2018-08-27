# Upload multiple text files into database table

cargs <- commandArgs(TRUE)
if (length(cargs) != 1) {
  stop("Usage: Rscript Upload_ArticleText_to-table.R directory")
}

library(RMySQL)

# connect to the database CPP
con = dbConnect(MySQL(), group = "CPP")

# Path to data files
path = cargs[1]
file.names <- dir(path, pattern = ".txt")

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
