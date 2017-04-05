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
import string
from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english')

# dict of source files, key file name, value the string of the file
sourcedict = {}
# dict of DH files
dhdict= {}
cfd = {}

directory = os.getcwd() + "/"

root = tkinter.Tk()
# set the title of the app
root.title(u"No Title at this point")

# create Listbox
lb = Listbox(root)
lbs = Listbox(root)
lbdh = Listbox(root, selectmode=MULTIPLE)

# create Scrollbar vertical and horizontal
sb1 = Scrollbar(root, orient = 'v', command = lb.yview)
sb2 = Scrollbar(root, orient = 'h', command = lb.xview)
ssb1 = Scrollbar(root, orient = 'v', command = lbs.yview)
ssb2 = Scrollbar(root, orient = 'h', command = lbs.xview)
dhsb1 = Scrollbar(root, orient = 'v', command = lbdh.yview)
dhsb2 = Scrollbar(root, orient = 'h', command = lbdh.xview)

# Listbox settings
lb.configure(yscrollcommand = sb1.set)
lb.configure(xscrollcommand = sb2.set)
lbs.configure(yscrollcommand = ssb1.set)
lbs.configure(xscrollcommand = ssb2.set)
lbdh.configure(yscrollcommand = dhsb1.set)
lbdh.configure(xscrollcommand = dhsb2.set)

lb.grid(row = 0, column = 0, sticky = 'nsew',  padx = 10, pady = 0,ipadx = 180,rowspan=6) # ipadx = 200, ipady = 140,
lbs.grid(row = 1, column = 2, pady = 0,padx=8,sticky = 'ns')#ipady = 40
lbdh.grid(row = 4, column = 2, pady = 0,padx=8, sticky = 'ns')#,ipady = 30

lbdh.configure(exportselection=False)
lbs.configure(exportselection=False)

sb1.grid(row = 0, column = 1, sticky = 'ns',rowspan=6)
sb2.grid(row = 6, column = 0, sticky = 'ew')
ssb1.grid(row = 1, column = 3, sticky = 'ns')
ssb2.grid(row = 2, column = 2, sticky = 'ew')
dhsb1.grid(row = 4, column = 3, sticky = 'ns')
dhsb2.grid(row = 5, column = 2, sticky = 'ew')

lbs_label = Label(root, text="Sources")
lbdh_label = Label(root, text="DH Files")

lbs_label.grid(row = 0, column = 2, pady = 5,padx=8,sticky = 'ew')
lbdh_label.grid(row = 3, column = 2, pady = 0,padx=8,sticky = 'ew')

option = BooleanVar()
option.set(True)
Checkbutton(text = 'Source with n:n', variable = option).grid(row = 6, column = 2, pady = 0,padx=8,sticky = 'ew')


# set entry box
buffer = StringVar()
buffer.set("20")

e = Entry(root, textvariable = buffer)
e.grid(row = 7, column = 0,columnspan = 2, sticky = 'ew',  padx = 10, pady = 10)

# the file type that the load methods accept
fTyp=[('text file','*.txt')]
# add methods
def load_source(event = ""):
    if os.path.isdir(directory+ "text"):
        iDir=directory + "text/"
    else:
        iDir=directory
    open_files(iDir, sourcedict,lbs)
    
def load_dh(event = ""):
    if os.path.isdir(directory+ "dh"):
        iDir=directory + "dh/"
    else:
        iDir=directory
    open_files(iDir, dhdict,lbdh)

def open_files(path, filedict, listbox):
    # does not loop any more for oppening files
    #oppening = True
    #while oppening:
    filenames=askopenfilenames(filetypes=fTyp,initialdir=path)
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
     #   else:
     #       oppening = False
    
def remove_source(event=""):
    if not lbs.get('active') is '':
        sourcedict.pop(lbs.get('active'))
        lbs.delete('active')
        lb.delete(0,END)
def remove_dh(event):
    if not lbdh.get('active') is '':
        dhdict.pop(lbdh.get('active'))
        lbdh.delete('active')
        lb.delete(0,END)

def remove_file(event = ""):
    iDir='c:/'
    fTyp=[('text file','*.txt')]
    file_directory=askopenfilename(filetypes=fTyp,initialdir=iDir)
    if file_directory is not "":
        filename = re.compile('\/[^/]+\.txt').findall(file_directory)[0]
        filename = filename[1:len(filename)-4]
        lb.delete(0,END)
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
    lb.delete(0,END)
    for s in text.split("\n"):
        lb.insert('end', s)
    

def create_dh_text(event=""):
    if not option.get():
        update_lb("DH is only for text with n:n")
        return
    if len(dhdict) == 0:
        update_lb("Need at least one DH file")
        return
    if lbs.curselection() == ():
        if len(sourcedict) == 0:
            update_lb("Need at least one Source file")
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
    for key in keys:
        text = ParseMarking(whole_text, dhdict[key])
        name =   key.split(" ")[0] + " " + lbs.get('active')
        iDir=directory
        if os.path.isdir(directory+ "text"):
            iDir=directory + "text/"
        file = open(iDir +name + '.txt','w')
        #file.write(name + "\n\n")
        content = name + "\n\n"
        for chap in sorted(text.keys()):
            for verse in sorted(text[chap].keys()):
                content += str(chap) + ":" + str(verse) + " " +text[chap][verse]
                file.write(content)
        file.close()
        sourcedict[name] = content
        dhdict.pop(key)
    remove_source()
    update_lb(content)
    lbdh.delete(0,END)
    lbs.delete(0,END)
    for key in dhdict:
        lbdh.insert('end', key)
    for key in sourcedict:
            lbs.insert('end', key)
        
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
    tup = []
    freqtup = []
    freqdict = {}
    for key in sourcedict:
        freqdict[key] = []
        content = sourcedict[key]
        # remove all the n:n
        content = (re.sub("\d+:\d+","",content))
        words = word_tokenize(content)
        for word in words:
            if not word.lower() in stopwords and not word.lower() in string.punctuation:
                tup.append((key,word))
    cfd = nltk.ConditionalFreqDist(tup)
    for key in cfd:
        tup = sorted(cfd[key].items(), key=itemgetter(1))
        thismuch = 20
        if buffer.get().isdigit():
            thismuch = int(buffer.get())
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

    freqcfd = nltk.ConditionalFreqDist(freqtup)
    freqcfd.plot()

# add methods to listbox
# Double click removes the file
lbs.bind('<Double-1>', remove_source)
lbdh.bind('<Double-1>', remove_dh)
lbs.bind('<Double-Button-3>', update_display_s)
# Right Double click displays the file
lbdh.bind('<Double-Button-3>', update_display_dh)

# control the bihavior of resising window
root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=1)
root.grid_rowconfigure(2,weight=1)

# adding menu
m = Menu(root)
root.configure(menu = m)
menu_file = Menu(m)
m.add_cascade(label='FILE',menu=menu_file,underline=0)
menu_file.add_command(label='Load Text',under=0,command=load_source)
menu_file.add_command(label='Load DH File',under=0,command=load_dh)
menu_file.add_command(label='Remove File',under=0,command=remove_file)

menu_dh = Menu(m)
m.add_cascade(label='DH',menu=menu_dh,underline=0)
menu_dh.add_command(label='Create',under=0,command=create_dh_text)

menu_cfd = Menu(m)
m.add_cascade(label='CFD',menu=menu_cfd,underline=0)
menu_cfd.add_command(label='Plot',under=0,command=plot_cfd)

# this starts the app
root.mainloop()
