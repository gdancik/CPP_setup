
USE DCAST;

set GLOBAL local_infile = "ON";

select "Creating DCAST.MeshTerms..." as '';

-- ------------------------------------------------------
--  DDL for MeshTerms table (we may split this into two 
--     tables) 
-- ------------------------------------------------------

DROP TABLE IF EXISTS DCAST.MeshTerms;
CREATE TABLE DCAST.MeshTerms(TreeID varchar(40), MeshID varchar(15), Term varchar(255));

# Import MeshTerms data from csv
select "Loading MeshTerms..." as '';
LOAD DATA LOCAL INFILE 'MeshTreeHierarchyWithScopeNotes.txt' 
INTO TABLE DCAST.MeshTerms COLUMNS TERMINATED BY '\t';

CREATE INDEX MeshTerms_IX1 ON DCAST.MeshTerms (TreeID, MeshID);
create index MeshTerms_IX2 on MeshTerms(MeshID);

update MeshTerms set Term = REPLACE(Term,'"','');

select "Filtering mesh terms..." as '';
delete from MeshTerms where TreeID not like 'C04%';
update meshterms set TreeID = 'C04.000', Term = 'Neoplasms (unspecified)' where TreeID = 'C04';

