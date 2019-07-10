use DCAST;

set GLOBAL local_infile = "ON";

select 'creating PubChem table...' as '' ;

DROP TABLE IF EXISTS DCAST.PubChem;

-- ------------------------------------------------------
--  DDL for Table PubChem
-- ------------------------------------------------------
  CREATE TABLE PubChem 
   (PMID INT NOT NULL, 
	  MeshID VARCHAR(15) NOT NULL, 
	  MENTIONS VARCHAR(800)
   ) ;


select 'loading PubChem table...' as '' ;

-- ------------------------------------------------------
--  Load data into PubChem 
-- ------------------------------------------------------
LOAD DATA LOCAL INFILE 'chemical2pubtator_processed' INTO TABLE PubChem IGNORE 1 LINES;

-- ------------------------------------------------------
--  DDL for Index PubChem_IX1
-- ------------------------------------------------------
select 'creating indices...' as '';
create INDEX PMIDIndex ON PubChem (PMID);
create INDEX MeshIndex ON PubChem (MeshID);

-- ------------------------------------------------------
--  Update PubChem to include only PMIDs in PubGene table  
--  and remove duplicates using group by  
-- ------------------------------------------------------

select 'filtering out non PubGene PMIDs...' as '';
SET SQL_SAFE_UPDATES = 0;
DELETE FROM PubChem WHERE NOT EXISTS
    (SELECT NULL FROM PubGene WHERE PubGene.PMID = PubChem.PMID);

-- ------------------------------------------------------
--  Update PubChem to include only pharmacologically  
--  active compounds
-- ------------------------------------------------------
select 'keeping only pharmacologically active compounds...' as '';
delete from PubChem
where PubChem.MeshID NOT IN
   (select MeshID from PharmActionTerms);

-- ------------------------------------------------------
--  Remove duplicates from PubChem
-- ------------------------------------------------------
select "Removing duplicates from PubChem..." as '';
CREATE TABLE tmp_data SELECT * FROM PubChem;
TRUNCATE TABLE PubChem;
ALTER TABLE PubChem ADD unique index idx_unique  (PMID, MeshID);
INSERT IGNORE INTO PubChem SELECT * from tmp_data;
DROP TABLE tmp_data;

