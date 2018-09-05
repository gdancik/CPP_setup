
DROP TABLE IF EXISTS DCAST.CancerTerms;

CREATE TABLE DCAST.CancerTerms
   (    TermID VARCHAR(20) NOT NULL,
        Term VARCHAR(25),
        Pattern VARCHAR(160),
        PRIMARY KEY (TermID)
   );

LOAD DATA LOCAL INFILE 'cancerterms.txt' 
INTO TABLE DCAST.CancerTerms 
IGNORE 1 LINES
(TermID, Term, Pattern, @dummy)
