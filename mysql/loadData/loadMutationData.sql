use DCAST;

set GLOBAL local_infile = "ON";

select 'creating PubMut table...' as '' ;

-- ------------------------------------------------------
--  DDL for Table PubMut
-- ------------------------------------------------------
  CREATE TABLE PubMut 
   (PMID INT NOT NULL, 
	  MutID VARCHAR(40) NOT NULL 
   ) ;


select 'loading PubMut table...' as '' ;

-- ------------------------------------------------------
--  Load data into PubMut 
-- ------------------------------------------------------
LOAD DATA LOCAL INFILE 'mutation2pubtator_processed' INTO TABLE PubMut 
IGNORE 1 LINES
(PMID, MutID, @dummy, @dummy);

-- ------------------------------------------------------
--  DDL for Index PubMut_IX1
-- ------------------------------------------------------
select 'creating indices...' as '';
create INDEX PMIDIndex ON PubMut (PMID);

####################################################
## update PubMut - only keep articles from PubMesh
###################################################
select 'keeping only PubMesh articles...' as '';
DELETE FROM PubMut
WHERE NOT EXISTS (
    SELECT PMID
    FROM PubMesh
    WHERE PubMesh.PMID = PubMut.PMID
);


