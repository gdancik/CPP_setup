use DCAST;

set GLOBAL local_infile = "ON";

select 'creating PubMut table...' as '' ;

-- ------------------------------------------------------
--  DDL for Table PubMut
-- ------------------------------------------------------
DROP TABLE IF EXISTS DCAST.PubMut;

CREATE TABLE PubMut 
   (PMID INT NOT NULL, 
	  MutID VARCHAR(40) NOT NULL 
   ) ;


select 'loading PubMut table...' as '' ;

-- ------------------------------------------------------
--  Load data into PubMut 
-- ------------------------------------------------------
LOAD DATA LOCAL INFILE 'mutation2pubtator_processed' INTO TABLE PubMut 
IGNORE 2 LINES;

-- ------------------------------------------------------
--  DDL for Index PubMut_IX1
-- ------------------------------------------------------
select 'creating indices...' as '';
create INDEX PMIDIndex ON PubMut (PMID);

-- ------------------------------------------------------
-- Keep only articles appearing in PubGene 
-- ------------------------------------------------------
/*
select 'keeping only PubGene articles...' as '';
DELETE FROM PubMut
WHERE NOT EXISTS (
    SELECT PMID
    FROM PubGene
    WHERE PubMut.PMID = PubGene.PMID
);
*/

-- ------------------------------------------------------
--  Update PubMut to remove duplicates   
-- ------------------------------------------------------

select "Removing duplicates from PubMut..." as '';
CREATE TABLE tmp_data SELECT * FROM PubMut;
TRUNCATE TABLE PubMut;
ALTER  TABLE PubMut ADD unique index idx_unique  (PMID, MutID);
INSERT IGNORE INTO PubMut SELECT * from tmp_data;
DROP TABLE tmp_data;


