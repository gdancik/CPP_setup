# this is a module to test whether a word is valid

import re
from nltk.corpus import stopwords
from nltk import SnowballStemmer
import string

snow = SnowballStemmer('english')
stop_words = stopwords.words('english') #load english stopwords


# returns a list of 'words' from a string, removing quotes and punctuation
def getWords(text) :
    pattern = re.compile("\'|\"|\-")
    text = pattern.sub('', text.lower())
    words = text.split()
   
    #remove punctuation
    table = str.maketrans('', '', string.punctuation)
    words = [w.translate(table) for w in words]
    return(words)            


# returns True if a 'word' is valid (not a number and at least 3 characters)
def testValid(word, stop_words):
    valid = True
    if word.isalnum() and not word.isdigit() and len(word) > 2:
        for w in stop_words:
            if w == word:
                valid = False
                break
    else:
        valid = False

    return valid

# converts a string to one containing only 'valid' terms
def stemWords(text) :
    w = getWords(text)
    w = [snow.stem(x) for x in w if testValid(x, stop_words)]
    return " ".join(w)



