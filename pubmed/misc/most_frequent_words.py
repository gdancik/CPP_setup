# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 17:25:31 2018

@author: kewilliams
"""

from operator import itemgetter

#csv file location
wordFile = r"C:/Users/kewil/pubmedXML/cancer_txt/cancer_words.csv"
commonWordFile = r"C:/Users/kewil/pubmedXML/cancer_txt/most_common_cancer_words.csv"
writeFile = open(commonWordFile, 'w')

words = []

for line in open(wordFile, 'r'):
    values = line.split(',')
    #threshold for removal of low occurance of words, improves looping dramatically
    if int(values[1]) >= 2000: #threshold for removal of low occurance of words, improves
        temp = (eval(values[0]), values[1].rjust(7, "0").strip())
        words.append(temp)

sorted_words = sorted(words, key = itemgetter(1), reverse = True)

for i in range(100): #desired number of words
    writeFile.write(ascii(sorted_words[i][0]) + "," + sorted_words[i][1].lstrip('0') + '\n')
    print("#" + str(i + 1) + " - " + sorted_words[i][0] \
          + " - " + sorted_words[i][1].lstrip('0'))
writeFile.close()