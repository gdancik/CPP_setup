USE DCAST;

set GLOBAL local_infile = "ON";

select "CREATING DCAST.PubMesh..." as '';
-- ------------------------------------------------------
--  DDL for Table PubMesh
-- ------------------------------------------------------
  CREATE TABLE DCAST.PubMesh 
   (PMID INT NOT NULL, 
	  MeshID VARCHAR(15) NOT NULL, 
	  MENTIONS VARCHAR(800)
   ) ;

-- ------------------------------------------------------
--  Load data into PubMesh 
-- ------------------------------------------------------
LOAD DATA LOCAL INFILE 'disease2pubtator_processed' INTO TABLE DCAST.PubMesh IGNORE 1 LINES;

-- ------------------------------------------------------
--  Update PubMesh to include only PMIDs in PubGene table  
--  and remove duplicates using group by  
-- ------------------------------------------------------
select "Filtering PubMesh based on PubGene..." as '';
create table t2 as SELECT PubMesh.PMID, PubMesh.MeshID 
   FROM PubMesh INNER JOIN PubGene ON PubGene.PMID = PubMesh.PMID
   GROUP BY PMID, MeshID;
   
drop table PubMesh;
rename table t2 to PubMesh;

# This is done in processing of disease2pubtator 
#select "Filtering PubMesh using Cancer...." as '';
#create table t2 as select PubMesh.PMID, PubMesh.MeshID from PubMesh inner join MeshTerms ON PubMesh.MeshID = MeshTerms.MeshID where MeshTerms.TreeID LIKE 'C04.%';
#drop table PubMesh;
#rename table t2 to PubMesh;

-- ------------------------------------------------------
--  DDL for Index PubMesh_IX1
-- ------------------------------------------------------
create INDEX PMIDIndex ON PubMesh (PMID);
create INDEX MeshIndex ON PubMesh (MeshID);

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



