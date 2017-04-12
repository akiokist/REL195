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

"rewrite"

# dict of source files, key file name, value the string of the file
sourcedict = {}
# dict of DH files
dhdict= {}
# save the current directory
directory = os.getcwd() + "/"

# save the fdist, key is the file name and the value is the fd dictionary
fdistdict = {}

root = tkinter.Tk()
# set the title of the app
root.title(u"No Title at this point")

# create Listbox
# main list box on the left
lb = Listbox(root)
# list box for source files on top right
lbs = Listbox(root)
# list box for dh files on bottum right
lbdh = Listbox(root, selectmode=MULTIPLE)

# create Scrollbar vertical and horizontal for each list box
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

# create a check box for two options
nn = BooleanVar()
nn.set(True)
Checkbutton(text = 'Source with "n:n"', variable = nn).grid(row = 6, column = 2, pady = 0,padx=8,sticky = 'w')
naming = BooleanVar()
naming.set(False)
Checkbutton(text = 'DH with "G F Marking"', variable = naming).grid(row = 7, column = 2, pady = 0,padx=8,sticky = 'w')

# set entry box
buffer = StringVar()
#buffer.set("20")
e = Entry(root, textvariable = buffer)
e.grid(row = 7, column = 0,columnspan = 2, sticky = 'ew',  padx = 20, pady = 7)

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

def plot_fd():
    fd = create_fd()
    if len(fd) > 0:
        fd.plot()

def plot_fd_percentile():
    fd = create_fd()
    wl = []
    d = {}
    if len(fd) > 0:
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
        

def create_fd():
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
        update_lb("DH is only for text with n:n")
        return
    if len(dhdict) == 0:
        update_lb("Need at least one DH file")
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
                        update_lb(dhname + " does not follow the naming rule.\n DH files must have 'one word group name' + 'Text file name' 'Marking' with spaces")
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
                content += str(chap) + ":" + str(verse) + " " +text[chap][verse]
        file.write(content)
        file.close()
        sourcedict[name] = content
    update_lb(content)
        #dhdict.pop(key)
    #sourcedict.pop(sourcename)
    
    #lbdh.delete(0,END)
    #lbs.delete(0,END)
    #for key in dhdict:
     #   lbdh.insert('end', key)
    #for key in sourcedict:
     #       lbs.insert('end', key)
        
def fileToDict(text):
    chapDict = {}
    length = len(text)
    i = 0
    if not text[0].isdigit():
        while i < length and not text[i].isdigit():
            i += 1
    start = i
    while i < length and text[i] != ":": #.isdigit():#  now goes as long there is an integer
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
    if len(freqcfd) > 0:
        freqcfd.plot()

def plot_cfd_percentile():
    freqcfd = create_cfd()
    if len(freqcfd) > 0:
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

# control the bihavior of resising window, see what happens when you change the size
root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=1)
root.grid_rowconfigure(2,weight=1)

# adding menu
m = Menu(root)
root.configure(menu = m)
menu_file = Menu(m)

# adding cascades to menu m
m.add_cascade(label='FILE',menu=menu_file,underline=0)
menu_file.add_command(label='Load Text',under=0,command=load_source)
menu_file.add_command(label='Load DH File',under=0,command=load_dh)
menu_file.add_command(label='Remove File',under=0,command=remove_file)

menu_dh = Menu(m)
m.add_cascade(label='DH',menu=menu_dh,underline=0)
menu_dh.add_command(label='Create',under=0,command=create_dh_text)

menu_cfd = Menu(m)
m.add_cascade(label='CFD',menu=menu_cfd,underline=0)
menu_cfd.add_command(label='Plot Value',under=0,command=plot_cfd)
menu_cfd.add_command(label='Plot Percentile',under=0,command=plot_cfd_percentile)
        
menu_fdist = Menu(m)
m.add_cascade(label='Fdist',menu=menu_fdist,underline=0)
menu_fdist.add_command(label='Plot Value',under=0,command=plot_fd)
menu_fdist.add_command(label='Plot Percentile',under=0,command=plot_fd_percentile)
# load text files from "text" folder if it exits
if os.path.isdir(directory+ "text"):
    file_directories = []
    for filename in os.listdir(directory + "text"):
        if filename.split(".")[-1] == "txt":
            file_directories.append(directory + "text/" + filename)        
    if len(file_directories) > 0:
        open_files(file_directories, sourcedict, lbs)


# load text files from "dh" folder if it exits
if os.path.isdir(directory+ "dh"):
    file_directories = []
    for filename in os.listdir(directory + "dh"):
        if filename.split(".")[-1] == "txt":
            file_directories.append(directory + "dh/" + filename)        
    if len(file_directories) > 0:
        open_files(file_directories, dhdict, lbdh)

if len(sourcedict) >0:
    update_lb(sourcedict[lbs.get(0)])

# this starts the app
root.mainloop()
