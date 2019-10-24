-- ------------------------------------------------------
--  Update PubCancerTerms to remove duplicates   
-- ------------------------------------------------------

select "Removing duplicates from PubCancerTerms..." as '';

CREATE TABLE tmp_data SELECT * FROM PubCancerTerms;
TRUNCATE TABLE PubCancerTerms;
ALTER  TABLE PubCancerTerms ADD unique index idx_unique  (PMID, TermID);
INSERT IGNORE INTO PubCancerTerms SELECT * from tmp_data;
DROP TABLE tmp_data;


