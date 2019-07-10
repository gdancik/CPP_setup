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
select "Removing PubGenes where genes are not in Genes table" as '';
SET SQL_SAFE_UPDATES = 0;
delete from PubGene 
where PubGene.GeneID NOT in 
    (select GeneID from Genes);

-- ------------------------------------------------------
--  Update PubGene to remove duplicates   
-- ------------------------------------------------------

select "Removing duplicates from PubGene..." as '';

CREATE TABLE tmp_data SELECT * FROM PubGene;
TRUNCATE TABLE PubGene;
ALTER  TABLE PubGene ADD unique index idx_unique  (GeneID, PMID);
INSERT IGNORE INTO PubGene SELECT * from tmp_data;
DROP TABLE tmp_data;

-- ------------------------------------------------------
--  Update Genes to include only GeneIDs with articles  
-- ------------------------------------------------------
select "Filtering Genes table based on articles..." as '';
delete from Genes
where Genes.GeneID NOT in
    (select distinct GeneID from PubGene);
