import os
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.book import *
from nltk.corpus import stopwords

stopwords = nltk.corpus.stopwords.words('english')


def stringToFile(s, name="result"):
    file = open(name + '.txt','w')
    file.write(s)
    file.close() 
    
def tupToFile(tup, name="result"):
    file = open(name + '.txt','w')
    for t in tup:
        file.write(" ".join(t) + "\n") 
    file.close() 


def lowAndUpTogether(fdist):
    listOfUpper = []
    for key in fdist.keys():
        if key[0].isupper() and key.lower() in fdist.keys():
            fdist[key.lower()] += fdist[key]
            listOfUpper.append(key) #fdist.pop(key, None)
    for x in range(len(listOfUpper)):
        fdist.pop(listOfUpper[x], None)
    return fdist
    
def printAll(fdist):
    s = ""
    from operator import itemgetter
    tup = sorted(fdist.items(), key=itemgetter(1))
    for key in tup:
        if not key[0].lower() in stopwords:
            if key[0].isalpha():
                print(key[0] + ":" + str(key[1]))
                s += key[0] + ":" + str(key[1]) + "\n"
    return s

def printFreq(fdist, moreThan):
    s = ""
    from operator import itemgetter
    tup = sorted(fdist.items(), key=itemgetter(1))
    for key in tup:
        if not key[0].lower() in stopwords:
            if key[0].isalpha() and key[1] > moreThan-1:
                print(key[0] + ":" + str(key[1]))
                s += key[0] + ":" + str(key[1]) + "\n"

    return s

def removeNoneAlpha(wordList):
    returnList = []
    for word in wordList:
        if word.isalpha():
            returnList.append(word)
    return returnList

def removeStopword(wordList):
    returnList = []
    for word in wordList:
        if not word in stopwords:
            returnList.append(word)
    return returnList

