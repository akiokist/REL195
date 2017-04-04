import os
import nltk
import sys
import re
from nltk.corpus import PlaintextCorpusReader
#from nltk.book import *
from nltk.corpus import stopwords
import string
from operator import itemgetter

directory = os.getcwd() + "/"
stopwords = nltk.corpus.stopwords.words('english')

allTexts =(
    PlaintextCorpusReader(directory + 'J Genesis.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'E Genesis.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Genesis.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'R Genesis.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'J Exodus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'E Exodus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Exodus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'R Exodus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Leviticus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'R Leviticus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'J Numbers.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'E Numbers.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Numbers.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'R Numbers.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'Dtr1 Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'Dtr2 Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'Dtn Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'E Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'Other Deuteronomy.txt', '.*').words(""))

#remove all n:n from text file
for text in allTexts:
    file = open(directory + text[0] + " " + text[1] + ".txt")
    s = (re.sub("\d+:\d+","",file.read()))
    file.close()
    file = open(directory + text[0] + " " + text[1] + ".txt", "w")
    file.write(s)
    file.close()

# reload the text files
allTexts =(
    PlaintextCorpusReader(directory + 'J Genesis.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'E Genesis.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Genesis.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'R Genesis.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'J Exodus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'E Exodus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Exodus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'R Exodus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Leviticus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'R Leviticus.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'J Numbers.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'E Numbers.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Numbers.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'R Numbers.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'Dtr1 Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'Dtr2 Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'Dtn Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'E Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'P Deuteronomy.txt', '.*').words(""),
    PlaintextCorpusReader(directory + 'Other Deuteronomy.txt', '.*').words(""))

genre_word = []
gentup = []

for text in allTexts:
    for word in text:
        if not word.lower() in stopwords and not word.lower() in string.punctuation:
            genre_word.append((text[0]+" "+text[1][:3],word))
            if text[1] == "Genesis":
                gentup.append((text[0]+" "+text[1][:3],word))
                

gencfd = nltk.ConditionalFreqDist(gentup)
cfd = nltk.ConditionalFreqDist(genre_word)

gentup = []
gencommondict = {}
for key in gencfd.keys():
    gencommondict[key] = []

for key in gencfd.keys():
    tup = sorted(cfd[key].items(), key=itemgetter(1))
    tup = tup[len(tup)-20:]
    for l in tup:
        gencommondict[key].append(l[0])
        for var in range(0, l[1]):
            gentup.append((key,l[0]))

for key in gencommondict.keys():
    for word in gencommondict[key]:
        for other in gencommondict.keys():
            if not key == other:
                if not word in gencommondict[other]:
                    gencommondict[other].append(word) 
                    if word in cfd[other]:
                        for var in range(0, cfd[other][word]):
                            gentup.append((other,word))
                            
gencfd = nltk.ConditionalFreqDist(gentup)

genre_word = []
for key in cfd.keys():
    tup = sorted(cfd[key].items(), key=itemgetter(1))
    tup = tup[len(tup)-20:]
    for l in tup:
        for var in range(0, l[1]):
            genre_word.append((key,l[0]))
    #cfds[key] = tup

cfdc = nltk.ConditionalFreqDist(genre_word)       

#for key in gencfd["R Gen"].keys():
#   print(key + ":" + str(gencfd["R Gen"][key]))

#print(cfd.conditions())
#print(cfd['E Exo'].most_common(20))

#for keys in cfd.keys():
    #for key in cfd[keys].keys():
        #print(keys + " " +key + ":" + str(cfd[keys][key]))

#for key in cfdc["J Gen"].keys():
#    print(key+":"+str(cfdc["J Gen"][key]))
