USE DCAST;

set GLOBAL local_infile = "ON";

select "CREATING DCAST.PubMesh..." as '';
-- ------------------------------------------------------
--  DDL for Table PubMesh
-- ------------------------------------------------------
DROP TABLE IF EXISTS DCAST.PubMesh;

CREATE TABLE DCAST.PubMesh 
   (PMID INT NOT NULL, 
	  MeshID VARCHAR(15) NOT NULL
   ) ;

-- ------------------------------------------------------
--  Load data into PubMesh 
-- ------------------------------------------------------
LOAD DATA LOCAL INFILE 'disease2pubtator_processed' INTO TABLE DCAST.PubMesh IGNORE 1 LINES;

-- ------------------------------------------------------
--  DDL for Index PubMesh_IX1
-- ------------------------------------------------------
create INDEX PMIDIndex ON PubMesh (PMID);
create INDEX MeshIndex ON PubMesh (MeshID);

-- ------------------------------------------------------
--  Update PubMesh to include only PMIDs in PubGene table  
--  and remove duplicates using group by  
-- ------------------------------------------------------

/*
select "Filtering PubMesh based on PubGene..." as '';
SET SQL_SAFE_UPDATES = 0;
delete from PubMesh
where PubMesh.PMID NOT in
    (select distinct PMID from PubGene);
*/

-- ------------------------------------------------------
--  Update PubGene to include only articles in PubMesh  
--  (i.e., only cancer-related)
-- ------------------------------------------------------
select "Filtering PubGene based on PubMesh..." as '';

DELETE FROM PubGene 
WHERE NOT EXISTS (
    SELECT PMID
    FROM PubMesh
    WHERE PubMesh.PMID = PubGene.PMID 
);


