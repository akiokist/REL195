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
import urllib
import unicodedata

biblename = "WEB" #"World English Bible"

# save the current directory
directory = os.getcwd()

def html_to_txt(files):
    files_size = len(files)
    file = None
    for index in range(0, files_size):
        match = re.search("<div class='mt'>([^/]+)</div>", files[index])
        if match != None:
            title = match.group(1).strip() + " " + biblename
            if file != None:
                file.close()
            file = create_new_file(title)
        before_after_chapter = re.split("<div class='chapterlabel' id=\"V0\">([^/]+)</div><div class=[^/]+>", files[index])
        if before_after_chapter != None and len(before_after_chapter) == 3:
            chapter = before_after_chapter[1].strip()
            after = re.split("</div><ul class='tnav'>", before_after_chapter[2])[0]
            write_chapter(file, chapter, after)
        else:
            print("does not have chapter")
            
def create_new_file(name):
    file = open(directory + "/" +name + '.txt','w')
    return file

def write_chapter(file, chapter, after):
    before_after_verse = re.split('<span class="verse" id="V', after)
    for verse in before_after_verse:
        verse_context = re.split("[^\d]+\d+;</span>", verse)
        if len(verse_context) == 2:
            verse_num = re.sub('">\d+',"",verse_context[0])
            content = re.sub("<a href=[^/]+span class[^/]+popup\">"," (",verse_context[1])
            content = re.sub("</span></a>",")",content)
            content = re.sub("</div><div class=[^/]+>","",content)
            content = re.sub("’","'",content)
            #if "—" in content[len(content)-3:]:
            #    print(content[len(content)-3:])
            content = re.sub("—","-",content)
            content = str(unicodedata.normalize('NFKD', content).encode('ascii','ignore'))
            content = chapter + ":" + verse_num + " " + content[2:-3] + "\n\n"
            file.write(content)
        else:
            print('[^\d]+\d+;</span> does not exist in :' + verse)


files = []
if os.path.isdir(directory + "/html"):
    path = directory + "/html"

for filename in os.listdir(path):
    if filename.split(".")[-1] == "htm":
        file = open(path + "/" + filename, 'r',encoding='utf-8') #’ 
        text = file.read()
        files.append(text)
        file.close()
        
html_to_txt(files)
