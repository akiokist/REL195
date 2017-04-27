import sys
import tkinter
import re
import os
from tkinter import *
import tkinter.filedialog
from tkinter.filedialog import *
from operator import itemgetter
import nltk
from nltk import word_tokenize
from nltk import FreqDist
import string
from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english')
import pylab as pl
import numpy as np
import tkinter.font
import enchant
english_words = enchant.Dict("en_US")

root = tkinter.Tk()
# set the title of the app
root.title("BOA") 
DH_FILE_CALLED = "Marking"
# dict of source files, key file name, value the string of the file
sourcedict = {}
# dict of DH files
dhdict= {}
# save the current directory
directory = os.getcwd() + "/"
# save the fdist, key is the file name and the value is the fd dictionary
fdistdict = {}

# create Listboxs
# now a Text on the left with font 11
lb = Text(root,state=DISABLED,font=("consolas",11),width=50,height=20)##Listbox(root,font=("consolas",11)) #Times
# list box for source files on top right
lbs = Listbox(root,height=8)
# list box for dh files on bottum right
lbdh = Listbox(root, selectmode=MULTIPLE,height=8)

# create Scrollbar vertical and horizontal for each list box
sb1 = Scrollbar(root, orient = 'v', command = lb.yview)
ssb1 = Scrollbar(root, orient = 'v', command = lbs.yview)
ssb2 = Scrollbar(root, orient = 'h', command = lbs.xview)
dhsb1 = Scrollbar(root, orient = 'v', command = lbdh.yview)
dhsb2 = Scrollbar(root, orient = 'h', command = lbdh.xview)
# add the Scrollbar to the Listbox
lb.configure(yscrollcommand = sb1.set)
lbs.configure(yscrollcommand = ssb1.set)
lbs.configure(xscrollcommand = ssb2.set)
lbdh.configure(yscrollcommand = dhsb1.set)
lbdh.configure(xscrollcommand = dhsb2.set)

lbdh.configure(exportselection=False)
lbs.configure(exportselection=False)

# set spin box
buffer = StringVar(root)
buffer.set("20")
n_spin = Spinbox(root, from_=1, to=999, textvariable=buffer,width=3)
# set serarch box
search_buffer = StringVar()
e = Entry(root, textvariable = search_buffer)
# create labels
lbs_label = Label(root, text="Sources")
lbdh_label = Label(root, text=DH_FILE_CALLED+" Files")
# create a check box for two options
nn = BooleanVar()
nn.set(True)
naming = BooleanVar()
naming.set(False)

# the file type that the load methods accept
fTyp=[('text file','*.txt')]
# add methods
def load_source(event = ""):
    if os.path.isdir(directory+ "text"):
        iDir=directory + "text/"
    else:
        iDir=directory
    open_files(askopenfilenames(filetypes=fTyp,initialdir=iDir), sourcedict,lbs)
    
def load_dh(event = ""):
    if os.path.isdir(directory+ "dh"):
        iDir=directory + "dh/"
    else:
        iDir=directory
    open_files(askopenfilenames(filetypes=fTyp,initialdir=iDir), dhdict,lbdh)

def open_files(filenames, filedict, listbox):
    if len(filenames) > 0:
        for file_directory in filenames:
            filename = re.compile('\/[^/]+\.txt').findall(file_directory)[0]
            filename = filename[1:len(filename)-4]
            if not filename in filedict:
                file = open(file_directory)
                filedict[filename] = file.read()
                text = filedict[filename]
                listbox.insert('end',filename)
                update_lb(text)
                file.close()
    
def remove_source(event=""):
    if not lbs.get('active') is '':
        sourcedict.pop(lbs.get('active'))
        lbs.delete('active')
        lb.delete(1.0,END)
def remove_dh(event):
    if not lbdh.get('active') is '':
        dhdict.pop(lbdh.get('active'))
        lbdh.delete('active')
        lb.delete(1.0,END)

def remove_file(event = ""):
    iDir='c:/'
    fTyp=[('text file','*.txt')]
    file_directory=askopenfilename(filetypes=fTyp,initialdir=iDir)
    if file_directory is not "":
        filename = re.compile('\/[^/]+\.txt').findall(file_directory)[0]
        filename = filename[1:len(filename)-4]
        lb.delete(1.0,END)
        if filename in sourcedict:
            sourcedict.pop(filename)
            lbs.delete(0,END)
            for key in sourcedict:
                lbs.insert('end',key)
        if filename in dhdict:
            dhdict.pop(filename)
            lbdh.delete(0,END)
            for key in dhdict:
                lbdh.insert('end',key)

def update_display_s(event):
    if not lbs.get('active') is '':
        update_lb(sourcedict[lbs.get('active')])
def update_display_dh(event):
    if not lbdh.get('active') is '':
        update_lb(dhdict[lbdh.get('active')])
def update_lb(text):
    lb.config(state=NORMAL)
    lb.delete(1.0,END)
    lb.insert('end',text)
    lb.config(state=DISABLED)

def plot_fd():
    fd = create_fd()
    if fd != None:
        fd.plot()

def plot_hapax():
    fd = create_fd(False)
    count = 0
    english_count = 0
    if fd != None:
        display_string = ""
        hapax = ""
        english_hapax = ""
        for word in fd:
            if english_words.check(word.lower()) and not re.match("\d",word):
                english_count = english_count +1
                if english_count % 8 ==0:
                    english_hapax += word + "\n"
                else:
                    english_hapax += word + ", "
            elif fd[word] == 1 and not re.match("\d",word) and not word[0] == "-"and not word[-1] == "-":
                count = count+1
                if count % 8 ==0:
                    hapax += word + "\n"
                else:
                    hapax += word + ", "
        if count > 0:
            display_string += "Hapax (words that only show up once)\n\n   There are " + str(count) +" non-English Hapax in this source\n\n" + hapax[:len(hapax)-2]
        if english_count > 0:
            display_string += "\n\n" + "    These are "+ str(english_count) +" English Hapax in this source\n\n" + english_hapax
        if count + english_count == 0:
            update_lb("Hapax (words that only show up once)\n\n" + "There were no Hapax in this source")
        else:
            update_lb(display_string)

def plot_fd_percentile():
    fd = create_fd()
    wl = []
    d = {}
    if fd != None:
        total = len(FreqDist(remove_stopwords(word_tokenize(sourcedict[lbs.get('active')]))))
        #print(str(total))
        for word in fd:
            p = (100 / total * fd[word])
            d[word] = p
            #print(word + ":" + str(fd[word]) + "::" + str(p))
        X = np.arange(len(d))
        pl.bar(X, d.values(), align='center', width=0.5)
        pl.xticks(X, d.keys())
        ymax = max(d.values()) + 1
        pl.ylim(0, ymax)
        pl.show()

def create_fd(use_buf=True):
    if lbs.curselection() == ():
        if len(sourcedict) == 0:
            update_lb("Need at least one Source file")
            return
        elif len(sourcedict) > 1:
            update_lb("Need to select one Source file")
            return
    thismuch = 20
    if buffer.get().isdigit():
        thismuch = int(buffer.get())
    filename = lbs.get('active')
    if use_buf == False:
        return FreqDist(remove_stopwords(word_tokenize(sourcedict[filename])))
    if filename in fdistdict:
        if len(fdistdict[filename]) > thismuch:
            fdistdict[filename] = common_fdist(fdistdict[filename], thismuch)
        else:
            fdistdict[filename] = FreqDist(remove_stopwords(word_tokenize(sourcedict[filename])))
            fdistdict[filename] = common_fdist(fdistdict[filename], thismuch)
        fd = fdistdict[filename]
    else:
        fd = FreqDist(remove_stopwords(word_tokenize(sourcedict[filename])))
        fd = common_fdist(fd, thismuch)
        fdistdict[filename] = fd
    return fd

def common_fdist(fd, thismuch):
    tup = sorted(fd.items(), key=itemgetter(1))
    tup = tup[len(tup)-thismuch:] # use variable
    wl = []
    for t in tup:
        for var in range(0, t[1]):
            wl.append(t[0])
    return FreqDist(wl)

def remove_stopwords(wl):
    returning_wl = []
    for word in wl:
        #word = word.lower()
        if not word.lower() in stopwords and not word.lower() in string.punctuation and not word.lower() == "'s" :
            returning_wl.append(word)
    return  returning_wl

def create_dh_text(event=""):
    if not nn.get():
        update_lb(DH_FILE_CALLED+" is only for text with n:n")
        return
    if len(dhdict) == 0:
        update_lb("Need at least one "+DH_FILE_CALLED+" file")
        return
    if lbs.curselection() == ():
        if len(sourcedict) == 0:
            update_lb("Need at least one Source file")
            return
        elif naming.get():
            # if DH file all has the form"groupname textname Marking" do it automaticlly
            d = {}
            for textname in sourcedict:
                keys = []
                for dhname in dhdict:
                    threeparts = dhname.split(" ")
                    if len(threeparts) > 2 and threeparts[-1] == "Marking":
                        if re.match(r"^"+" ".join(threeparts[1:-1]), textname):#" ".join(threeparts[1:-1]) in textname:
                            keys.append(dhname)
                    else:
                        update_lb(dhname + " does not follow the naming rule.\n"+DH_FILE_CALLED+" files must have 'one word group name' + 'Text file name' 'Marking' with spaces")
                        return
                if len(keys) > 0:
                    d[textname] = keys
            for textname in d:
                whole_text = fileToDict(sourcedict[textname])
                create_dh_source(textname,whole_text, d[textname])
            remove_files(d)
            return
        elif len(sourcedict) > 1:
            update_lb("Need to select one Source file")
            return
    # if there is only one source file, even if it is not selected
    # it will use that source
    whole_text = fileToDict(sourcedict[lbs.get('active')])
    keys = []
    if lbdh.curselection() == ():
        keys = list(dhdict.keys())
    else:
        for index in lbdh.curselection():
            keys.append(lbdh.get(index))
    create_dh_source(lbs.get('active'),whole_text, keys)
    remove_files({lbs.get('active'):keys})

def remove_files(d):
    for textname in d:
        for dhname in d[textname]:
            if dhname in dhdict:
                dhdict.pop(dhname)
        sourcedict.pop(textname)
    lbdh.delete(0,END)
    lbs.delete(0,END)
    for key in dhdict:
        lbdh.insert('end', key)
    for key in sourcedict:
        lbs.insert('end', key)
        
def create_dh_source(sourcename,whole_text, keys):
    for key in keys:
        text = ParseMarking(whole_text, dhdict[key])
        name =   key.split(" ")[0] + " " + sourcename
        iDir=directory
        if os.path.isdir(directory+ "text"):
            iDir=directory + "text/"
        file = open(iDir +name + '.txt','w')
        content = name + "\n\n"
        for chap in sorted(text.keys()):
            for verse in sorted(text[chap].keys()):
                # if no two new line character at the end, add it
                if text[chap][verse][len(text[chap][verse])-2:] != "\n\n":
                    content += str(chap) + ":" + str(verse) + " " +text[chap][verse] + "\n\n"
                else:
                    content += str(chap) + ":" + str(verse) + " " +text[chap][verse]
        file.write(content)
        file.close()
        sourcedict[name] = content
    update_lb(content)
        
def fileToDict(text):
    chapDict = {}
    length = len(text)
    i = 0
    if not text[0].isdigit():
        while i < length and not text[i].isdigit():
            i += 1
    start = i
    while i < length and text[i] != ":": #.isdigit():#  now goes as long as  there is an integer
        i += 1
    while i < length:
        currentChap = int(text[start:i])
        chapDict[currentChap] = {}
        # check if it is still the same chapter
        while i < length and currentChap == int(text[start:i]):
            end_of_verse = False
            i += 1
            start = i
            while i < length and text[i].isdigit():
                i += 1
            currentVerse = int(text[start:i])
            start = i
            #set i to be the end of this verse
            while not end_of_verse:
                while i < length and not text[i].isdigit():
                    i += 1
                end = i
                while i < length and text[i].isdigit():
                    i += 1
                if i >= length:
                    chapDict[currentChap][currentVerse] = text[start:i]
                    break # end of file
                if text[i] == ":":
                    i = end
                    end_of_verse = True
            chapDict[currentChap][currentVerse] = text[start:i]
            start = i
            while i < length and text[i] != ":":#.isdigit():# 
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
    return create_newsorce(fromList, toList, text)

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

def create_newsorce(fromList, toList, text):
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

def dictToFile(text, name):
    file = open(name + '.txt','w')
    file.write(name + "\n\n")
    for chap in sorted(text.keys()):
        for verse in sorted(text[chap].keys()):
            file.write(str(chap) + ":" + str(verse) + " ")
            file.write(text[chap][verse])
    file.close()
    
def plot_cfd():
    freqcfd = create_cfd()
    if freqcfd != None:
        freqcfd.plot(title='Conditional Frequency Distribution')

def plot_cfd_percentile():
    freqcfd = create_cfd()
    if freqcfd != None:
        for filename in freqcfd:
            total = len(remove_stopwords(word_tokenize(sourcedict[filename])))
            for word in freqcfd[filename]:
                p = 100 / total * freqcfd[filename][word]
                freqcfd[filename][word] = p
        freqcfd.plot()

def create_cfd():
    thismuch = 20
    if buffer.get().isdigit():
        thismuch = int(buffer.get())
    tup = []
    freqtup = []
    freqdict = {}
    for key in sourcedict:
        freqdict[key] = []
        content = sourcedict[key]
        # remove all the n:n
        if nn.get():
            content = (re.sub("\d+:\d+","",content))
        words = remove_stopwords(word_tokenize(content))
        for word in words:
            tup.append((key,word))
    cfd = nltk.ConditionalFreqDist(tup)
    for key in cfd:
        tup = sorted(cfd[key].items(), key=itemgetter(1))        
        tup = tup[len(tup)-thismuch:] # use variable
        for l in tup:
            freqdict[key].append(l[0])
            for var in range(0, l[1]):
                    freqtup.append((key,l[0]))
    for key in freqdict:
        for word in freqdict[key]:
            for other in freqdict.keys():
                if not key == other:
                    if not word in freqdict[other]:
                        freqdict[other].append(word) 
                        if word in cfd[other]:
                            for var in range(0, cfd[other][word]):
                                freqtup.append((other,word))
    return nltk.ConditionalFreqDist(freqtup)

# add methods to listbox
# Double click removes the file
lbs.bind('<Double-1>', remove_source)
lbdh.bind('<Double-1>', remove_dh)
# Right Single click to displays the content of the file "now Single Click"
lbs.bind('<Button-3>', update_display_s)
lbdh.bind('<Button-3>', update_display_dh)

# adding menu
m = Menu(root)
root.configure(menu = m)
menu_file = Menu(m)

# adding cascades to menu m
m.add_cascade(label='FILE',menu=menu_file,underline=0)
menu_file.add_command(label='Load Text',under=0,command=load_source)
menu_file.add_command(label="Load "+DH_FILE_CALLED+" File",under=0,command=load_dh)
menu_file.add_command(label='Remove Sources',under=0,command=remove_file)

menu_dh = Menu(m)
m.add_cascade(label=DH_FILE_CALLED,menu=menu_dh,underline=0)
menu_dh.add_command(label='Apply',under=0,command=create_dh_text)

menu_cfd = Menu(m)
m.add_cascade(label='CFD',menu=menu_cfd,underline=0)
menu_cfd.add_command(label='Plot by Value',under=0,command=plot_cfd)
menu_cfd.add_command(label='Plot by Percentage',under=0,command=plot_cfd_percentile)
        
menu_fdist = Menu(m)
m.add_cascade(label='Fdist',menu=menu_fdist,underline=0)
menu_fdist.add_command(label='Plot by Value',under=0,command=plot_fd)
menu_fdist.add_command(label='Plot by Percentage',under=0,command=plot_fd_percentile)
menu_fdist.add_command(label='Plot Hapax',under=0,command=plot_hapax)

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
from nltk.metrics.spearman import *

def bigram():
    if lbs.curselection() == ():
        if len(sourcedict) == 0:
            update_lb("Need at least one Source file")
            return
        elif len(sourcedict) > 1:
            update_lb("Need to select one Source file")
            return
    thismuch = 20
    if buffer.get().isdigit():
        thismuch = int(buffer.get())    
    filename = lbs.get('active')
    wl = [w.lower() for w in word_tokenize(sourcedict[filename])]
    bcf = BigramCollocationFinder.from_words(wl)
    if bcf == None:
        return
    stop = set(stopwords)
    filter_stop = lambda w:len(w)<3 or w in stop
    bcf.apply_word_filter(filter_stop)
    bcf = sorted(bcf.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
    bcf = bcf[:thismuch]
    word_pairs = []
    word_values = []
    odd =False
    for tup in bcf:
        pair = ""
        if odd:
            pair = "\n"
            odd = False
        else:
            odd = True
        pair += tup[0][0] + " " +  tup[0][1]
        word_pairs.append(pair)
        word_values.append(int(tup[1]))
    X = np.arange(len(word_values))
    pl.bar(X, word_values, align='center', width=0.5)
    pl.xticks(X, word_pairs)
    ymax = max(word_values) + 1
    pl.ylim(0, ymax)
    pl.show()

# lots of code duplication, nice if it can be removed someday
def trigram():
    if lbs.curselection() == ():
        if len(sourcedict) == 0:
            update_lb("Need at least one Source file")
            return
        elif len(sourcedict) > 1:
            update_lb("Need to select one Source file")
            return
    thismuch = 20
    if buffer.get().isdigit():
        thismuch = int(buffer.get())    
    filename = lbs.get('active')
    wl = [w.lower() for w in word_tokenize(sourcedict[filename])]
    bcf = TrigramCollocationFinder.from_words(wl)
    if bcf == None:
        return
    stop = set(stopwords)
    filter_stop = lambda w:len(w)<3 or w in stop
    bcf.apply_word_filter(filter_stop)
    bcf = sorted(bcf.ngram_fd.items(), key=lambda t: (-t[1], t[0]))
    bcf = bcf[:thismuch]
    word_pairs = []
    word_values = []
    row = 0
    for tup in bcf:
        pair = ""
        if row == 0:
            row = 1
        elif row == 1:
            pair = "\n"
            row = 2
        else:
            pair = "\n\n"
            row = 0
        pair += tup[0][0] + " " +  tup[0][1] + " " + tup[0][2]
        word_pairs.append(pair)
        word_values.append(int(tup[1]))
    X = np.arange(len(word_values))
    pl.bar(X, word_values, align='center', width=0.5)
    pl.xticks(X, word_pairs)
    ymax = max(word_values) + 1
    pl.ylim(0, ymax)
    pl.show()
# add the n-gram menu    
menu_n_gram = Menu(m)
m.add_cascade(label='N-Gram',menu=menu_n_gram,underline=0)
menu_n_gram.add_command(label='Bigram',under=0,command=bigram)
menu_n_gram.add_command(label='Trigram',under=0,command=trigram)

def concordance():
    if lbs.curselection() == ():
        if len(sourcedict) == 0:
            update_lb("Need at least one Source file")
            return
        elif len(sourcedict) > 1:
            update_lb("Need to select one Source file")
            return
    thismuch = 5
    if buffer.get().isdigit():
        thismuch = int(buffer.get())
    filename = lbs.get('active')
    text = sourcedict[filename]
    display_result = ""
    search_word = search_buffer.get().lower()
    if search_word == "":
        return
    lb.config(state=NORMAL)
    lb.delete(1.0,END)
    if nn.get():
        text_dict =  fileToDict(text)
        for chap in text_dict:
            for verse in text_dict[chap]:
                word = text_dict[chap][verse]
                if re.match("[^\n]*"+search_word+"[^\n]*",word.lower()):
                    three = re.match("([^\n]*)("+search_word+")([^\n]*)",word.lower()).groups()
                    firsthalf = three[0]
                    match = three[1]
                    rest =three[2]
                    lb.insert('end',str(chap)+":"+str(verse)+firsthalf)
                    lb.insert('end',match,'search')
                    lb.insert('end',rest+"\n\n")
    else:
        wl = word_tokenize(text)
        start = thismuch
        end = len(wl)-thismuch
        for index in range(0,start):
            if re.match("[^\n]*"+search_word+"[^\n]*", wl[index].lower()):
                lb.insert('end',wl[0])
                for i in range(1,index):
                    if wl[i] in string.punctuation:
                        lb.insert('end',wl[i])
                    else:
                        lb.insert('end'," " + wl[i])
                lb.insert(re.match('end',"([^\n]*)("+search_word+")([^\n]*)",wl[index].lower()).groups()[1],'search')
                lb.insert('end',"\n\n")
        for  index in range(start,end):
            if  re.match("[^\n]*"+search_word+"[^\n]*", wl[index].lower()):
                lb.insert('end',wl[index-thismuch])
                for i in range(index-thismuch+1,index):
                    if wl[i] in string.punctuation:
                        lb.insert('end',wl[i])
                    else:
                        lb.insert('end', " "+wl[i])
                lb.insert('end',re.match("([^\n]*)("+search_word+")([^\n]*)",wl[index].lower()).groups()[1],'search')
                for i in range(index+1,index+thismuch+1):
                    if wl[i] in string.punctuation:
                        lb.insert('end',wl[i])
                    else:
                        lb.insert('end', " "+wl[i])
                lb.insert('end',"\n\n")
        for  index in range(end,end+thismuch):
            if  re.match("[^\n]*"+search_word+"[^\n]*", wl[index].lower()):
                lb.insert('end',re.match("([^\n]*)("+search_word+")([^\n]*)",wl[index].lower()).groups()[1],'search')
                lb.insert('end',wl[end])
                for i in range(end+1,end+index):
                    if wl[i] in string.punctuation:
                        lb.insert('end',wl[i])
                    else:
                        lb.insert('end', " "+wl[i])
                lb.insert('end',"\n\n")
                #display_result += " ".join(wl[index:])
                #display_result +="\n\n"
    #lb.config(state=NORMAL)
    #lb.tag_configure("search", background = '#F0B325')
    #lb.delete(1.0,END)
    #for word in result_list:
     #   if search_word in word:
      #      lb.insert('end',word,)
       # else:
       #     lb.insert('end',word)
       # lb.insert('end',word,'search')
    lb.config(state=DISABLED)
    #update_lb(display_result)
    
menu_concordance  = Menu(m)
m.add_cascade(label='Concordance',menu=menu_concordance,underline=0)
menu_concordance.add_command(label='Search',under=0,command=concordance)

#methods for help
def marking_help():
    update_lb("\nMarking files are lists of chapters and verses that define Pentateuchal sources.\n"+
              "These could be individual verses or a span of contiguous verses.\n"
              "The file contents appear, for example, as\n\n"+
              " 1:7,\n 1:13-14,\n 2:23.8-2:25.99,\n (...)\n\n"+
              "With the filename denoting a particular source, such as “P Exodus Marking.”\n"+
              "To use the Marking function, the user chooses a book of the Bible from the\n"+
              "“Sources” box, and a marking file from the “Marking Files” box,\n"+
              "then select Apply in the Marking toolbar menu. The results will display those\n"+
              "Bible verses corresponding to the user-selected source text."
              )

def fd_help():
    update_lb("\nFdist, or Frequency Distribution, is a method that tallies the occurrence of every word in a given corpus and returns the ones that occur most frequently in graphical form. The default value is 20, which means the 20 most common words will be listed in the results, though this can be changed in the input field."+
              "\n\nTo use it, select a book of the Bible from the Sources box and choose one of the three plotting options:\n\n"+
              "1. Plot by Value: \n"+
              "2. Plot by Percentage:\n"
              "3. Plot Hapax: Short for “hapax legomenon,” a term in corpus linguistics for any word in a corpus that occurs only once. Choosing this method will not return a graph but a list of all hapax legomena for a given book of the Bible in the primary display box.")

def cfd_help():
    update_lb("CFD, or Conditional Frequency Distribution, operates much like Fdist, with the\n\n"+
              "Plot by Value: raw hits\n\n"+
              "Plot by Percentage: relative to the size of the text (100%), the word tallies relative to the size of the text.")


def concordance_help():
    update_lb("\n"+"The concordance function takes a word from the input field and, if the word exists in the selected corpus, each occurrence of the word is displayed along with its surrounding context. As well as its verse and chapter location.")

menu_help = Menu(m)
m.add_cascade(label='Help',menu=menu_help,underline=0)
menu_help.add_command(label=DH_FILE_CALLED,under=0,command=marking_help)
menu_help.add_command(label='FD',under=0,command=fd_help)
menu_help.add_command(label='CFD',under=0,command=cfd_help)
menu_help.add_command(label='Concordance',under=0,command=concordance_help)

# if there is a setting file load that to set up the settings
if os.path.exists(directory + "setting.txt"):
    set_text = open(directory + "setting.txt").read()
    if re.match('[^/]*Sources with "n:n"[^\n]*=[^\n]*False',set_text):
        nn.set(False)
    if re.match('[^/]*Marking with "G F Marking"[^\n]*=[^\n]*True',set_text):
        naming.set(True)
    if not re.match('[^/]*Load Marking automatically[^\n]*=[^\n]*False',set_text):
        # load text files from "dh" folder if it exits
        if os.path.isdir(directory+ "dh"):
            file_directories = []
            for filename in os.listdir(directory + "dh"):
                if filename.split(".")[-1] == "txt":
                    file_directories.append(directory + "dh/" + filename)        
        if len(file_directories) > 0:
            open_files(file_directories, dhdict, lbdh)
    if not re.match('[^/]*Load Sources automatically[^\n]*=[^\n]*False',set_text):
        # load text files from "text" folder if it exits
        if os.path.isdir(directory+ "text"):
            file_directories = []
            for filename in os.listdir(directory + "text"):
                if filename.split(".")[-1] == "txt":
                    file_directories.append(directory + "text/" + filename)        
            if len(file_directories) > 0:
                open_files(file_directories, sourcedict, lbs)
    if re.match('[^/]*default numbe[^\n]*(\d+)',set_text):
        buffer.set(int(re.search('[^/]*default numbe[^\d\n]*(\d+)',set_text).group(1)))
    if re.match('[^/]*default search word[^\n]*=[^\n]*"([^\n]+)"',set_text):
        search_buffer .set(re.search('[^/]*default search word[^\n]*=[^\n]*"([^\n]+)"',set_text).group(1))

# set the welcome screen
lb.tag_configure("search", background = '#F0B325')
lb.config(state=NORMAL)
lb.delete(1.0,END)
lb.insert('end',"   ____   ___    _     ",'search')
lb.insert('end',"\n")
lb.insert('end', "  | __ ) / _ \  / \    " ,'search')
lb.insert('end',"\n")
lb.insert('end',"  |  _ \| | | |/ _ \   ",'search')
lb.insert('end',"\n")
lb.insert('end',"  | |_) | |_| / ___ \  ",'search')
lb.insert('end',"\n")
lb.insert('end',"  |____/ \___/_/   \_\ ",'search')
lb.insert(
          'end',
          "\n\nWelcome to BOA, the Biblical Origins Analyzer! This program gathers together several text analysis tools from the Python-based NLTK (Natural Language Toolkit) suite into one easy-to-use space for Torah scholars doing compositional analysis.\n\n"+
          "BOA was constructed around the documentary hypothesis (DH) of Pentateuchal biblical scholarship, that \n"+
          "the Pentateuch as we have it today originated as four separate textual sources, the Yahwist (J), Elohist (E), Deuteronomic (D) and Priestly (P) sources, which were combined\n\n"+
          "That the Pentateuch was originally four separate sources that were combined over time \n"+
          "For example, Genesis 1:1-2:3, which constitutes the seven day Creation account, is considered syntactically different enough from the rest of Genesis 2 that documentary hypothesis scholars have judged the two sections to have been composed at different times by different writers."
          "\n\nCreated by Akio Kist-Okazaki and Tristan Engel."
          )
lb.config(state=DISABLED)
# set the size of things
lb_size = 180
# 40% each, total 80 %
side_ld_size =  int(lb_size/2.5)
# 5% each 20% total
reg_size = int(lb_size/20)
lb_size = lb_size-reg_size
left = 30
right = 10
pad = 3
search_width = int(left/1.5)
spin_width = int(left/6)

# create button for search
search_button = Button(root, text = 'Search', command = concordance)
# set the grid
# left side top to down
lb.grid(row = 0, column = 0, sticky = 'nsew',  padx = pad, pady = pad,rowspan=lb_size,columnspan= left) # ipadx = 200, ipady = 140,
sb1.grid(row = 0, column = left, sticky = 'ns',rowspan=lb_size)
e.grid(row = lb_size+1, column = 0,columnspan = search_width, sticky = 'ew',  padx = 10, pady = 7,rowspan=reg_size)
search_button.grid(row = lb_size+1, column = search_width,columnspan = spin_width, sticky = 'ew',  padx = 2, pady = 2,rowspan=reg_size)
n_spin.grid(row = lb_size+1, column = search_width+spin_width+1,columnspan = spin_width, sticky = 'ew',  padx = 2, pady = 2,rowspan=reg_size)

#right side top to down
lbs_label.grid(row = 0, column = left+1, pady = pad,padx=pad,sticky = 'ew',rowspan=reg_size,columnspan=right)
lbs.grid(row =  reg_size+1,column = left+1, pady = 0,padx=0,sticky = 'ns',rowspan=side_ld_size-reg_size,columnspan=right)#ipady = 40
ssb1.grid(row =  reg_size+1,column = right +left, sticky = 'ns',columnspan=right,rowspan=side_ld_size-reg_size)
ssb2.grid(row =  side_ld_size+1, column = left+1, sticky = 'ew',rowspan=reg_size,padx=pad,columnspan=right)
Checkbutton(text = 'Source with "n:n"', variable = nn).grid(row = side_ld_size+reg_size+1, column = left+1, pady = 0,padx=8,sticky = 'w',rowspan=reg_size,columnspan=right)
lbdh_label.grid(row = int(reg_size *2+side_ld_size+1), column = left+1, pady = 0,padx=8,sticky = 'ew',rowspan=reg_size,columnspan=right)
lbdh.grid(row = int(reg_size *3+side_ld_size+1), column = left+1, pady = 0,padx=8, sticky = 'ns',rowspan=side_ld_size-reg_size,columnspan=right)#,ipady = 30
dhsb1.grid(row = int(reg_size *3+side_ld_size+1), column = right+left, sticky = 'ns',rowspan=side_ld_size)
dhsb2.grid(row = int(reg_size *2+side_ld_size*2+1),column = left+1,sticky = 'ew',rowspan=reg_size,columnspan=right,padx=pad)
Checkbutton(text = 'DH with "G F Marking"', variable = naming).grid(row = int(reg_size *3+side_ld_size*2+1), column = left+1, pady = 0,padx=8,sticky = 'w',rowspan=reg_size,columnspan=right)

# control the bihavior of resising window, see what happens when you change the size
for i in range(0, lb_size):
    root.grid_rowconfigure(i,weight=1)
for i in range(0, left+right):
    root.grid_columnconfigure(i,weight=1)

# this starts the app
root.mainloop()
