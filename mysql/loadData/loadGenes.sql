/*!40000 DROP DATABASE IF EXISTS `dcast`*/;

select "CREATING DATABASE..." as '';
CREATE DATABASE DCAST;

set GLOBAL local_infile = "ON";

USE DCAST;

select "CREATING DCAST.GENES..." as '';
-- ------------------------------------------------------
--  DDL for Table GENE
-- ------------------------------------------------------
CREATE TABLE DCAST.GENES
   (	GeneID INT NOT NULL, 
    	SYMBOL VARCHAR(20),
        PRIMARY KEY (GeneID)
   );


-- ------------------------------------------------------
--  load data into Table GENE
-- ------------------------------------------------------

LOAD DATA LOCAL INFILE 'HumanGeneIDs.csv' INTO TABLE Genes 
  COLUMNS TERMINATED BY ',' IGNORE 1 lines;

UPDATE Genes set SYMBOL = REPLACE(Symbol, '\r','');

-- ------------------------------------------------------
--  DDL for Index GENE_IX1
-- ------------------------------------------------------
  CREATE INDEX GENE_IX1 ON DCAST.GENES (GeneID);

