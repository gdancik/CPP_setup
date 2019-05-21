

# s = col_to_set('HumanGeneIDs.csv', ',',0)
def col_to_set(file, sep, index, header = True) :
    """
    returns a set from specified column of file
       file: file to be opened
       sep: the column separator
       index: index of column of interest, starting at 0
       header: True if 1st row is a header
    """
    f = open(file)
    if header :
        f.readline()
    s = {line.split(sep)[index] for line in f }
    return s
    
