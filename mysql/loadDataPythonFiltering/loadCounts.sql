-- ------------------------------------------------------
--  Create 'Counts' tables with total articles per ID 
-- ------------------------------------------------------

-- ------------------------------------------------------
--  Create MeshCounts 
-- ------------------------------------------------------

CREATE INDEX idx_Counts_MeshID ON MeshCounts (MeshID);


-- ------------------------------------------------------
--  Create GeneCounts 
-- ------------------------------------------------------

select 'Creating GeneCounts' as '';

DROP TABLE IF EXISTS DCAST.GeneCounts;

CREATE TABLE GeneCounts as
SELECT 
    GeneID, COUNT(DISTINCT PMID) as Count
FROM
    PubGene
GROUP BY GeneID;

CREATE INDEX idx_Counts_GeneID ON GeneCounts (GeneID);


-- ------------------------------------------------------
--  Create ChemCounts 
-- ------------------------------------------------------

select 'Creating ChemCounts' as '';

DROP TABLE IF EXISTS DCAST.ChemCounts;

CREATE TABLE ChemCounts as
SELECT 
    MeshID, COUNT(DISTINCT PMID) as Count
FROM
    PubChem
GROUP BY MeshID;

CREATE INDEX idx_Counts_MeshID ON ChemCounts (MeshID);


-- ------------------------------------------------------
--  Create MutCounts 
-- ------------------------------------------------------

select 'Creating MutCounts' as '';

DROP TABLE IF EXISTS DCAST.MutCounts;

CREATE TABLE MutCounts as
SELECT
    MutID, COUNT(DISTINCT PMID) as Count
FROM
    PubMut
GROUP BY MutID;

CREATE INDEX idx_Counts_MutID ON MutCounts (MutID);


-- ------------------------------------------------------
--  Create CancerTermCounts 
-- ------------------------------------------------------

select 'Creating CancerTermCounts' as '';

DROP TABLE IF EXISTS DCAST.CancerTermCounts;

CREATE TABLE CancerTermCounts as
SELECT
    TermID, COUNT(DISTINCT PMID) as Count
FROM
    PubCancerTerms
GROUP BY TermID;

CREATE INDEX idx_Counts_TermID ON CancerTermCounts (TermID);

