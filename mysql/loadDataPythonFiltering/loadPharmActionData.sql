use DCAST;

-- ------------------------------------------------------
--  DDL for Table PubChem
-- ------------------------------------------------------
DROP TABLE IF EXISTS DCAST.PharmActionTerms;

CREATE TABLE PharmActionTerms 
   ( MeshID VARCHAR(15) NOT NULL, 
	  Term VARCHAR(300)
   ) ;

select 'created PharmActionTerms table' as '' ;

-- ------------------------------------------------------
--  Load data into PubChem 
-- ------------------------------------------------------
LOAD DATA LOCAL INFILE 'paList.txt' INTO TABLE PharmActionTerms; 

select 'loaded PharmActionTerms table' as '' ;


-- ------------------------------------------------------
--  DDL for Index PharmActionTerms
-- ------------------------------------------------------
create INDEX MeshIndex ON PharmActionTerms (MeshID);

select 'created indices' as '';

select 'DONE' as '';



-- ------------------------------------------------------
--  Update PharmActionTerms to remove duplicates   
-- ------------------------------------------------------

select "Removing duplicates from PharmActionTermse..." as '';

CREATE TABLE tmp_data SELECT * FROM PharmActionTerms;
TRUNCATE TABLE PharmActionTerms;
ALTER  TABLE PharmActionTerms ADD unique index idx_unique  (MeshID, Term);
INSERT IGNORE INTO PharmActionTerms SELECT * from tmp_data;
DROP TABLE tmp_data;


