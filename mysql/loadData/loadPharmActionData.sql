use DCAST;

-- ------------------------------------------------------
--  DDL for Table PubChem
-- ------------------------------------------------------
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

