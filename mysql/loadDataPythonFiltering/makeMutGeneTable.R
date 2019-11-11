library(RMariaDB)

####################################################
# let's allow multiple
####################################################

con <- dbConnect(MariaDB(), group = "CPP")

muts <- dbGetQuery(con, "select distinct MutID from PubMut")

n <- nrow(muts)
res <- data.frame(NULL)
genes <- vector("integer", n)


for (i in seq_along(muts$MutID)) {
  cat("finding gene for mut #", i, "/",n,"\n")
  m <- muts$MutID[i]
  qry <- paste0("
        select Genes.Symbol,count(PubGene.GeneID) as Frequency from PubGene
        inner join Genes on Genes.GeneID = PubGene.GeneID
        where PMID in (select distinct PMID from PubMut where MutID = '", m, "')
        group by PubGene.GeneID order by Frequency desc limit 10;")
  
  r <- dbGetQuery(con, qry)
  
  g <- r$Symbol[r$Frequency == max(r$Frequency)]
  
  genes[i] <- paste(g, collapse = ",")

}


dbDisconnect(con)

d <- data.frame(MutID = muts$MutID, Genes = genes, stringsAsFactors = FALSE)


# cat("press a key to continue...\n")
# scan(file = "", what= character())


################################################
# create table
################################################

con <- dbConnect(MariaDB(), group = "CPP")

dbExecute(con, "DROP TABLE IF EXISTS MutGene;")

qry <- "CREATE TABLE DCAST.MutGene
(    MutID VARCHAR(40) NOT NULL,
  Genes VARCHAR(100) NOT NULL,
  PRIMARY KEY (MutID)
);"

dbExecute(con, qry)

dbAppendTable(con, "MutGene", d)

dbDisconnect(con)


