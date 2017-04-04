import sys
import tkinter
import re
import os
from tkinter import *
import tkinter.filedialog
from tkinter.filedialog import *

# dict of source files, key file name, value the string of the file
sourcedict = {}
# dict of DH files
dhdict= {}
cfd = {}

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

# set entry box
buffer = StringVar()
buffer.set("20")

e = Entry(root, textvariable = buffer)
e.grid(row = 7, column = 0,columnspan = 2, sticky = 'ew',  padx = 10, pady = 10)

# add methods
def load_text(event = ""):
    iDir='c:/'
    fTyp=[('text file','*.txt')]
    file_directory=askopenfilename(filetypes=fTyp,initialdir=iDir)
    if file_directory is not "":
        filename = re.compile('\/[^/]+\.txt').findall(file_directory)[0]
        filename = filename[1:len(filename)-4]
        file = open(file_directory)
        sourcedict[filename] = file.read()
        text = sourcedict[filename]
        lbs.insert('end',filename)
        lb.delete(0,END)
        for s in text.split("\n"):
            lb.insert('end', s)
        file.close()

def load_dh(event = ""):
    iDir='c:/'
    fTyp=[('text file','*.txt')]
    file_directory=askopenfilename(filetypes=fTyp,initialdir=iDir)
    if file_directory is not "":
        filename = re.compile('\/[^/]+\.txt').findall(file_directory)[0]
        filename = filename[1:len(filename)-4]
        file = open(file_directory)
        dhdict[filename] = file.read()
        text = dhdict[filename]
        lbdh.insert('end',filename)
        lb.delete(0,END)
        for s in text.split("\n"):
            lb.insert('end', s)
        file.close()

def remove_source(event):
    if not lbs.get('active') is '':
        sourcedict.pop(lbs.get('active'))
        lbs.delete('active')
        lb.delete(0,END)
def remove_dh(event):
    if not lbdh.get('active') is '':
        dhdict.pop(lbdh.get('active'))
        lbdh.delete('active')
        lb.delete(0,END)

def update_display_s(event):
    if not lbs.get('active') is '':
        text = sourcedict[lbs.get('active')]
        lb.delete(0,END)
        for s in text.split("\n"):
                lb.insert('end', s)
def update_display_dh(event):
    if not lbdh.get('active') is '':
        text = dhdict[lbdh.get('active')]
        lb.delete(0,END)
        for s in text.split("\n"):
                lb.insert('end', s)
    

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
menu_file.add_command(label='Load Text',under=0,command=load_text)
menu_file.add_command(label='Load DH File',under=0,command=load_dh)

root.mainloop()
