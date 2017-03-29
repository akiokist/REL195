import os
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.book import *
from nltk.corpus import stopwords

directory = os.getcwd() + "/"

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
        genre_word.append((text[0]+" "+text[1][:3],word))

cfd = nltk.ConditionalFreqDist(genre_word)
