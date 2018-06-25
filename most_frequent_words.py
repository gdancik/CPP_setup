# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 17:25:31 2018

@author: kewil
"""

wordDict = {}

#csv file location
wordFile = open(r"C:/Users/kewil/PubMedXML/cancer_txt/cancer_words.csv")
commonWordFile = r"C:/Users/kewil/PubMedXML/cancer_txt/most_common_cancer_words.csv"
writeFile = open(commonWordFile, 'w')

for line in wordFile:
    values = line.split(',')
    #threshold for removal of low occurance of words, improves looping dramatically
    if int(values[1]) >= 2000: #threshold for removal of low occurance of words, improves
        
        #fill dictionary with words and the number of articles they occur in
        #need rjust for sorting the count of words -- 0987 > 0099 vs 987 < 99
        wordDict[eval(values[0])] = values[1].rjust(7, "0")
    
#sort dictionary values from largest to smallest
greatestValues = sorted(wordDict.values(), reverse=True)

#loop through dictionary to find most common words
#unable to do a get or find value since there may be duplicate values
index = 0
count = 1
while count <= 100:
    for key in wordDict:
        if wordDict[key] == greatestValues[index]:
            writeFile.write(key + "," + greatestValues[index].lstrip('0'))
            print("#" + str(count) + " - " + key \
                  + " - " + greatestValues[index].lstrip('0'))
            count += 1
    index += 1
writeFile.close()