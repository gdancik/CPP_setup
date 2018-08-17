########################################################################
# Reformat tmVar style mutations from mutation2pubator, using the
# nomenclature at http://varnomen.hgvs.org/. Examples:
#   Substitution: c|SUB|C|435|G -> c.C435G
#   Deletion: p|DEL|508|F -> p.F508del
#   Insertion: p|INS|1795|D -> p.1795insD
#   Duplication: "c|DUP|1285_1301|| -> c.1285-1301dup	 	
#   p.A3dup (single amino acid) or p.A3_S6dup (multiple amino acids)
#   Frameshift: p|FS|G|46|5| -> p.G46fs5
########################################################################

library(dplyr)

cargs <- commandArgs(TRUE)
if (length(cargs) != 2) {
  stop("Usage: R processMutations2pubtator.R --no-save --args infile outFile")
}

###############################################################################
# Substitution functions
###############################################################################
formatSubstitution <- function(mutTerm) {
  # format nucleotide substitutions
  g <- grepl("\\|SUB\\|", mutTerm) & grepl("^c\\||^g\\||^m\\||^r\\|", mutTerm)
  if (any(g)) {
    mutTerm[g] <- gsub("\\|SUB", ".", mutTerm[g])
    s <- strsplit(mutTerm[g], "\\|")
    reformatted <- sapply(s, formatSubstitutionAfterSplit)
    mutTerm[g] <- reformatted 
  }
  
  # format protein substitutions
  g <- grepl("\\|SUB\\|", mutTerm) & grepl("^p\\|", mutTerm)
  if (any(g)) {
    mutTerm[g] <- gsub("\\|SUB\\|", ".", mutTerm[g])
    mutTerm[g] <- gsub("\\|", "", mutTerm[g])
  }
  return(mutTerm)
}

formatSubstitutionAfterSplit <- function(x) {
  if (length(x) != 4) {
    #stop("invalid format -- ", paste0(x, collapse = "|"))
    return(paste0(x, collapse = "|"))
  }
  return(paste0(x[1], x[3], x[2], ">", x[4]))
}


###############################################################################
# Deletion functions
###############################################################################
formatDeletionAfterSplit <- function(x) {
  if (length(x) != 4) {
    #stop("invalid format -- ", paste0(s, collapse = "|"))
    return(paste0(x, collapse = "|"))
  }
  
  if (x[1] == "") {
    x[1] = "?"
  }
  return(paste0(x[1], ".", x[4], x[3], "del"))
} 


formatDeletion <- function(mutTerm) {
  
  # protein deletion
  g <- grepl("DEL", mutTerm) & grepl("^p\\|", mutTerm)
  if (any(g)) {
    s <- strsplit(mutTerm[g], "\\|")
    reformatted <- sapply(s, formatDeletionAfterSplit)
    mutTerm[g] <- reformatted 
  }
  
  # nucleotide deletion
  g <- grepl("DEL", mutTerm) & grepl("^c\\||^g\\||^m\\||^r\\|", mutTerm)
  if (any(g)) {
    mutTerm[g] <- gsub("\\|", "", mutTerm[g])
    mutTerm[g] <- gsub("DEL", ".", mutTerm[g])
  }
  
  return(mutTerm)
}


###############################################################################
# Frameshift functions
###############################################################################
formatProteinFrameShift <- function(mutTerm) {
  g <- grepl("\\|FS\\|", mutTerm)
  if(any(g)) {
    # mutTerm[g] <- gsub(";.+", "", mutTerm)
    x <- mutTerm[g]
    s <- strsplit(x,"\\|")
    
    mutTerm[g] <- sapply(s, processFSSplit)
    
  }
  
  return(mutTerm)
}

processFSSplit <- function(x1) {
  if (length(x1) < 4) {
    return(paste0(x1, collapse = "|"))
  } else if (length(x1) == 4) {
    res <- paste0(x1[1], ".", x1[3], x1[4], "fs")
  } else {
    res <- paste0(x1[1], ".", x1[3], x1[4], x1[5], "fs")
    if (length(x1) == 6) {
      res <- paste0(res, "Ter", x1[6])
    }
  }
  res
}


###############################################################################
# Insertions 
###############################################################################
formatProteinAndNucleoInsertion <- function(mutTerm) {
  g <- grepl("\\|INS\\|",mutTerm)
  if (any(g)) {
    mutTerm[g] <- gsub("\\|INS\\|", ".", mutTerm[g])
    mutTerm[g] <- gsub("\\|", "ins", mutTerm[g])
  }
  
  return(mutTerm)
}



###############################################################################
# INDELS
###############################################################################
formatProteinAndNucleoDeletionInsertion <- function(mutTerm) {
  g <- grepl("\\|INDEL\\|", mutTerm)
  if (any(g)) {
    mutTerm[g] <- gsub("\\|INDEL\\|", ".", mutTerm[g])
    mutTerm[g] <- gsub("\\|", "delins", mutTerm[g])
  }
  return(mutTerm)
}


###############################################################################
# Duplications
###############################################################################
formatProteinAndNucleoDuplication <- function(mutTerm) {
  g <- grepl("\\|DUP\\|", mutTerm)
  if (any(g)) {
    x <- mutTerm[g]
    s <- strsplit(x, "\\|")
    s <- sapply(s, formatDupFromSplit)
    mutTerm[g] <- s
  }
  
  return(mutTerm)
}

# Note: tmVar may include additional information at x[5], supposedly num dups but
# this is usually not the case. For now we ignore it.
formatDupFromSplit <- function(x) {
  if (length(x) < 4) {
    return(paste0(x, collapse = "|"))
  }
  res <- paste0(x[1], ".", x[3], "dup", x[4])
  res
}

###############################################################################
# Main Program
###############################################################################

infile <- cargs[1]
outfile <- cargs[2]
f = read.delim(infile, sep = "\t", header = TRUE, colClasses = "character")
f <- filter(f,  grepl("^RS", f$Components, ignore.case = TRUE) == FALSE) 
mutTerm <- f$Components

# remove trailing RS information
mutTerm <- gsub(";RS.+", "", mutTerm)

# format mutations
mutTerm <- formatSubstitution(mutTerm)
mutTerm <- formatDeletion(mutTerm)
mutTerm <- formatProteinFrameShift(mutTerm)
mutTerm <- formatProteinAndNucleoInsertion(mutTerm)
mutTerm <- formatProteinAndNucleoDeletionInsertion(mutTerm)
mutTerm <- formatProteinAndNucleoDuplication(mutTerm)

# convert nucleotide mutations to lowercase
h <- grepl("^r.", mutTerm)
mutTerm[h] <- tolower(mutTerm[h])

f$Components = mutTerm

write.table(f, file = outfile, sep = "\t", row.names = FALSE, quote = FALSE)


