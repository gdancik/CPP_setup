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
--  Update PubChem to include only PMIDs in PubGene table  
--  and remove duplicates using group by  
-- ------------------------------------------------------
select 'filtering out non PubGene PMIDs...' as '';
create table t2 as SELECT PubChem.PMID, PubChem.MeshID 
   FROM PubChem INNER JOIN PubGene ON PubGene.PMID = PubChem.PMID
   GROUP BY PMID, MeshID;
   
drop table PubChem;
rename table t2 to PubChem;


####################################################
## update PubChem - keep only associations with 
##    pharmacologically active compounds
###################################################

create table t2 as SELECT PubChem.PMID, PubChem.MeshID 
   FROM PubChem INNER JOIN 
   PharmActionTerms ON PharmActionTerms.MeshID = PubChem.MeshID;

drop table PubChem;
rename table t2 to PubChem;

-- ------------------------------------------------------
--  Update PharmAction table to include only MeshIDs in PubChem table  
--  and remove duplicates using group by  
-- ------------------------------------------------------
select 'filter out non PubChem MeshIDs' as '';
create table t2 as SELECT  PharmActionTerms.MeshID, PharmActionTerms.Term 
   FROM PharmActionTerms INNER JOIN PubChem ON PharmActionTerms.MeshID = PubChem.MeshID
   GROUP BY PharmActionTerms.MeshID, PharmActionTerms.Term;
   
drop table PharmActionTerms;
rename table t2 to PharmActionTerms;

-- ------------------------------------------------------
--  DDL for Index PubChem_IX1
-- ------------------------------------------------------
select 'creating indices...' as '';
create INDEX PMIDIndex ON PubChem (PMID);
create INDEX MeshIndex ON PubChem (MeshID);

