import os
import nltk
import sys
import re
from nltk.corpus import PlaintextCorpusReader
#from nltk.book import *
from nltk.corpus import stopwords

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

for text in allTexts:
    for word in text:
        if not word.lower() in stopwords:
            genre_word.append((text[0]+" "+text[1][:3],word))

cfd = nltk.ConditionalFreqDist(genre_word)

# these were only here for test purpose
#sss = "1:1 the 20:20 all"
#sss = re.sub("\d+:\d+","",sss)
#print(sss)
#print(cfd.conditions())
#print(cfd['E Exo'].most_common(20))
