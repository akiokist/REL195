import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.book import *
from nltk.corpus import stopwords
import CreateBibleDHtext
from CreateBibleDHtext import * 
import printAll
from printAll import * 
direc = os.getcwd() + "/"

gene1 = createSubBible([[1,1,0]], [[2,4,0]], BibleDict["Genesis"])
dictToFile(gene1, "genesis1")
gene2 = createSubBible([[2,5,0]], [[3,24,0]], BibleDict["Genesis"])
dictToFile(gene2, "genesis2")
fdist1 = FreqDist(PlaintextCorpusReader(direc + "genesis1.txt", '.*').words(""))
fdist2 = FreqDist(PlaintextCorpusReader(direc + "genesis2.txt", '.*').words(""))

fdist1 = lowAndUpTogether(fdist1)
fdist2 = lowAndUpTogether(fdist2)

#printFreq(fdist1,10)
#printFreq(fdist2,10)

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

list1 = [w.lower() for w in PlaintextCorpusReader(direc + "genesis1.txt", '.*').words("")]
list2 = [w.lower() for w in PlaintextCorpusReader(direc + "genesis2.txt", '.*').words("")]

list1 = removeNoneAlpha(list1)
list2 = removeNoneAlpha(list2)
#list1 = removeStopword(list1)
#list2 = removeStopword(list2)

bcf1 = BigramCollocationFinder.from_words(list1)
bcf2 = BigramCollocationFinder.from_words(list2)

b1 = bcf1.nbest(BigramAssocMeasures.likelihood_ratio, 100)
b2 = bcf2.nbest(BigramAssocMeasures.likelihood_ratio, 100)

tupToFile(b1, "gene1 bigram")
tupToFile(b2, "gene2 bigram")

from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures

tcf1 = TrigramCollocationFinder.from_words(list1)
tcf2 = TrigramCollocationFinder.from_words(list2)

t1 = tcf1.nbest(TrigramAssocMeasures.likelihood_ratio, 100)
t2 = tcf2.nbest(TrigramAssocMeasures.likelihood_ratio, 100)

tupToFile(t1, "gene1 trigram")
tupToFile(t2, "gene2 trigram")
