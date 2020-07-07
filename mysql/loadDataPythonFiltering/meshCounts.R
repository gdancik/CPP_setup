con = dbConnect(MariaDB(), group = "CPP")
treeIDs <- dbGetQuery(con, 'Select * from MeshTerms where TreeID like "C04%";')
dbDisconnect(con)


s <- split(treeIDs$TreeID, treeIDs$MeshID)

counts <- integer(length(s))

con = dbConnect(MariaDB(), group = "CPP")
for (i in 1:length(s)) {
  msg <- paste0('counting number of articles for ', names(s)[i], '...')
  print(msg)
  qry <- paste0("select  count(distinct PMID) as count  from PubMesh  inner join MeshTerms ON
    MeshTerms.MeshID = PubMesh.MeshID where ", 
                paste0('TreeID like "', s[[i]], '%"', collapse = " OR "),
                ";"
  )
 
  res <- dbGetQuery(con, qry)
  counts[i] <- as.integer(res$count[1])
}

dbDisconnect(con)

d <- data.frame(MeshID = as.character(names(s)), Count = as.integer(counts),
                stringsAsFactors = FALSE)

con <- dbConnect(MariaDB(), group = "CPP")

dbExecute(con, "DROP TABLE IF EXISTS MeshCounts;")

qry <- "CREATE TABLE DCAST.MeshCounts
(    MeshID VARCHAR(40) NOT NULL,
  Count BIGINT(21) NOT NULL,
  PRIMARY KEY (MeshID)
);"

dbExecute(con, qry)

dbAppendTable(con, "MeshCounts", d)

dbDisconnect(con)


