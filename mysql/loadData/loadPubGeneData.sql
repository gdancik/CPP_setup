USE DCAST;

set GLOBAL local_infile = "ON";

select "Creating DCAST.PubGene..." as '';
-- ------------------------------------------------------
--  DDL for Table PubGene  
-- ------------------------------------------------------
DROP TABLE IF EXISTS DCAST.PubGene;

CREATE TABLE DCAST.PubGene 
   (	PMID INT  NOT NULL, 
	    GeneID INT NOT NULL
   ) ;

-- ------------------------------------------------------
--  Load data into PubGene  
-- ------------------------------------------------------
select "Loading PubGene..." as '';
LOAD DATA LOCAL INFILE 'gene2pubtator_processed' INTO TABLE DCAST.PubGene IGNORE 1 LINES;

select "Building indices..." as '';
-- ------------------------------------------------------
--  DDL for Index PubGene_IX1
-- ------------------------------------------------------
CREATE INDEX PubGene_IX1 ON DCAST.PubGene (GeneID, PMID);

-- ------------------------------------------------------
--  DDL for Index PubGene_IX2
-- ------------------------------------------------------
CREATE INDEX PubGene_IX2 ON DCAST.PubGene (PMID);



-- ------------------------------------------------------
--  Update PubGene to include only GeneIDs in Genes table  
-- ------------------------------------------------------
select "Filtering PubGene based on Genes table..." as '';
create table t2 as select PubGene.GeneID, PubGene.PMID from PubGene 
inner join Genes on PubGene.GeneID = Genes.GeneID;

drop table PubGene;
rename table t2 to PubGene;

-- ------------------------------------------------------
--  Update PubGene to remove duplicates   
-- ------------------------------------------------------
select "Removing duplicates from PubGene..." as '';
create table t2 as select GeneID, PMID  from PubGene
GROUP BY GeneID, PMID;
drop table PubGene;
rename table t2 to PubGene;


-- ------------------------------------------------------
--  Update Genes to include only GeneIDs with articles  
-- ------------------------------------------------------
select "Filtering Genes table based on articles..." as '';
create table t2 as select Genes.GeneID, Genes.SYMBOL from Genes 
inner join PubGene on Genes.GeneID = PubGene.GeneID group by Genes.GeneID, Genes.SYMBOL;
drop table Genes;
rename table t2 to Genes;

