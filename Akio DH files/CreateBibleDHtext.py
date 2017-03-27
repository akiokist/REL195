import re
import os
import sys

directory = os.getcwd() + "/"

def setDirectory(dir):
    directory = dir
    if directory[-1] != "/":
       directory += "/"
    return directory

# first open all the markings
def loadMarkings(markings, directory):
    markings['J Genesis'] = open(directory + 'J Genesis Marking.txt')
    markings['E Genesis'] =  open(directory + 'E Genesis Marking.txt')
    markings['P Genesis'] = open(directory + 'P Genesis Marking.txt')
    markings['R Genesis'] = open(directory + 'R Genesis Marking.txt')
    markings['J Exodus'] = open(directory + 'J Exodus Marking.txt')
    markings['E Exodus'] = open(directory + 'E Exodus Marking.txt')
    markings['P Exodus'] = open(directory + 'P Exodus Marking.txt')
    markings['R Exodus'] = open(directory + 'R Exodus Marking.txt')
    markings['P Leviticus'] = open(directory + 'P Leviticus Marking.txt')
    markings['R Leviticus'] = open(directory + 'R Leviticus Marking.txt')
    markings['J Numbers'] = open(directory + 'J Numbers Marking.txt')
    markings['E Numbers'] = open(directory + 'E Numbers Marking.txt')
    markings['P Numbers'] = open(directory + 'P Numbers Marking.txt')
    markings['R Numbers'] = open(directory + 'R Numbers Marking.txt')
    markings['Dtr1 Deuteronomy'] = open(directory + 'Dtr1 Deuteronomy Marking.txt')
    markings['Dtr2 Deuteronomy'] = open(directory + 'Dtr2 Deuteronomy Marking.txt')
    markings['Dtn Deuteronomy'] = open(directory + 'Dtn Deuteronomy Marking.txt')
    markings['E Deuteronomy'] =  open(directory + 'E Deuteronomy Marking.txt')
    markings['P Deuteronomy'] =  open(directory + 'P Deuteronomy Marking.txt')
    markings['Other Deuteronomy'] = open(directory + 'Other Deuteronomy Marking.txt')

markings = {}
loadMarkings(markings, directory)

Genesis = open(directory + 'Genesis.txt').read()
Exodus = open(directory + 'Exodus.txt').read()
Leviticus = open(directory + 'Leviticus.txt').read()
Numbers = open(directory + 'Numbers.txt').read()
Deuteronomy = open(directory + 'Deuteronomy.txt').read()
Bible = {"Genesis" : Genesis, "Exodus" : Exodus, "Leviticus" : Leviticus, "Numbers": Numbers, "Deuteronomy": Deuteronomy}

def fileToDict(text):
    chapDict = {}
    length = len(text)
    i = 0
    if not text[0].isdigit():
        while i < length and not text[i].isdigit():
            i += 1
    start = i
    while i < length and text[i] != ":":
        i += 1
    while i < length:
        currentChap = int(text[start:i])
        chapDict[currentChap] = {}
        while i < length and currentChap == int(text[start:i]):
            i += 1
            start = i
            while i < length and text[i].isdigit():
                i += 1
            currentVerse = int(text[start:i])
            start = i
            while i < length and not text[i].isdigit():
                i += 1
            chapDict[currentChap][currentVerse] = text[start:i]
            if i >= length:
                break # end of file
            # check if it is still the same chapter
            start = i
            while i < length and text[i] != ":":
                i += 1
    return chapDict

def ParseMarking(text, marking):
    fromList = []
    toList = []
    if marking[-1] == ".":
        marking =  marking[:-1] # remove the final "." from  marking
    tokens = marking.replace(" ", "").replace("\n", "").split(",")
    for token in tokens:
        token += "-"
        i = 0
        mid = 0
        while token[i] != "-":
            i += 1
        textFrom = getChapVerWord(token[:i+1])
        if len(token) != i+1:        
            i += 1
            mid = i
            if ":" in token[mid:]:
                while token[i] != "-":
                    i += 1
                textTo = getChapVerWord(token[mid:])
            else :
                textTo = [0,int(token[mid:-1]),0]
        else:
            textTo = [0,0,0]
        fromList.append(textFrom)
        toList.append(textTo)
    return createSubBible(fromList, toList, text)

def getChapVerWord(token):
    chap = 0 # chapter number
    verse = 0 # verse number
    word = 0
    i = 0
    indexOfIdentifier = 0
    while token[i].isdigit():
        i = i+1
    if token[i] == ":":
        chap = int(token[:i]) # convert the string up to ":" to int as the chapter number
        indexOfIdentifier = i
        i = i+1
        while token[i].isdigit():
            i = i+1
            if token[i] == "-":
                verse = int(token[indexOfIdentifier+1:i]) # ":" between "-" is the verse number
            if token[i] == ".":
                verse = int(token[indexOfIdentifier+1:i]) # ":" between "." is the verse number
                indexOfIdentifier = i
                i = i+1
                while token[i].isdigit():
                    i = i+1
                if token[i] == "-":
                    word = int(token[indexOfIdentifier+1:i]) # ":" between "." is the verse number
    return [chap,verse,word]
    
def createSubBible(fromList, toList, text):
    subD = {}
    for i in range(len(fromList)):
        fromChap = fromList[i][0]
        toChap = toList[i][0]
        fromVerse = fromList[i][1]
        toVerse = toList[i][1]
        if not fromChap in subD:
                subD[fromChap] = {} 
        if toVerse == 0:
            if fromList[i][2] > 0:
                if fromVerse in text[fromChap]:
                    subD[fromChap][fromVerse] = getWordFrom(text[fromChap][fromVerse],fromList[i][2])
            else:
                if fromVerse in text[fromChap]:
                    subD[fromChap][fromVerse] = text[fromChap][fromVerse]
        elif toChap == 0:
            # do not need to care about "."
            for inner in range (fromVerse,toVerse+1):
                if inner in text[fromChap]:
                    if inner in text[fromChap]:
                        subD[fromChap][inner] = text[fromChap][inner]
        elif fromChap == toChap:
            if fromList[i][2] > 0:
                if fromVerse in text[fromChap]:
                    subD[fromChap][fromVerse] = getWordFrom(text[fromChap][fromVerse],fromList[i][2])
            else:
                if fromVerse in text[fromChap]:
                    subD[fromChap][fromVerse] = text[fromChap][fromVerse]
            for inner in range (fromVerse+1,toVerse):
                if inner in text[fromChap]:
                    subD[fromChap][inner] = text[fromChap][inner]
            if toList[i][2] > 0:
                if toVerse in text[fromChap]:
                    subD[fromChap][toVerse] = getWordTo(text[fromChap][toVerse],toList[i][2])
            else:
                if toVerse in text[fromChap]:
                    subD[fromChap][toVerse] = text[fromChap][toVerse] 
        else:
            # get the from chapter verses, using from verse
            for inner in range (fromVerse, len(text[fromChap])+1):
                if inner in text[fromChap]:
                    subD[fromChap][inner] = text[fromChap][inner]    
            for outer in range (fromChap+1, toChap):
                currentChap = outer
                if not currentChap in subD:
                    subD[currentChap] = {}
                for inner in range (1, len(text[currentChap])+1):
                    if inner in text[currentChap]:
                        subD[currentChap][inner] = text[currentChap][inner]
            if not toChap in subD:
                    subD[toChap] = {}
            # get the to chapter verses, using to verse
            for inner in range (1, toVerse+1):
                if inner in text[toChap]:
                    subD[toChap][inner] = text[toChap][inner]    
    return subD                  
                
def getWordFrom(verse,wordIndex):
    restList = verse.strip().split(" ")[wordIndex-1:]
    return " ".join(restList) + "\n\n"

def getWordTo(verse,wordIndex):
    restList = verse.strip().split(" ")[:wordIndex]
    return " ".join(restList) + "\n\n"

def dictToString(text):
    stringText = ""
    for chap in text.keys():
        for verse in text[chap].keys():
            stringText += text[chap][verse]
    return stringText
        
def tokenize(text): # meaningless since PlaintextCorpusReader does this
    stringText = dictToString(text)
    return list(filter(None, stringText.replace("!", " ").replace("?", " ").replace("\n", " ").replace(".", " . ").replace(",", " , ").replace(";", " ; ").replace(":", " : ").split(" ")))

def printChapAndVerse(text):
    for key in text.keys():
        print("Chapter "+ str(key) + " : Verses: " + str(text[key].keys()))

def dictToFile(text, name):
    file = open(name + '.txt','w')
    file.write(name + "\n\n")
    for chap in sorted(text.keys()):
        for verse in sorted(text[chap].keys()):
            file.write(str(chap) + ":" + str(verse) + " ")
            file.write(text[chap][verse])
    file.close() 

BibleDict = {"Genesis":fileToDict(Bible["Genesis"]), "Exodus":fileToDict(Bible["Exodus"]), "Leviticus":fileToDict(Bible["Leviticus"]), "Numbers":fileToDict(Bible["Numbers"]), "Deuteronomy":fileToDict(Bible["Deuteronomy"])}
subBible = {}
for key in markings.keys():
    subBible[key] = ParseMarking(BibleDict[key.split(" ")[1]], markings[key].read())
    dictToFile(subBible[key], key)
loadMarkings(markings, directory) # reload these so that it can be seen




