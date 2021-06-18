'''
Created on Jul 31, 2020

@author: crusty-cast

A frame widget which contains an entry widget, used to display the path; and button widget, used to open
up a file explorer.
'''

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from math import floor
from os.path import basename as fileName

class FileLoader(tk.Frame):
    '''
    Frame widget containing an entry and button.

    Used by the user to open a file.
    '''


    def __init__(self, master, rFiles = [("Image File", ".png .jpg .tga")], strFileTitle = "Open", font = None, *args, **kwargs):
        '''
        Constructor
        '''
        self.master = master
        self.rFiles = rFiles
        self.strFileTitle = strFileTitle

        self.width = kwargs.get("width", 300)
        self.height = kwargs.get("height", 25)

        kwargs["width"] = self.width
        kwargs["height"] = self.height
        super().__init__(master, *args, **kwargs)

        self.pEntryTextVar = tk.StringVar()
        self.pEntry = tk.Entry(self, state = "readonly", textvariable = self.pEntryTextVar)
        if font:
            self.pEntry.config(font = font)
            #self.height = font[1] + 18
            self.config(height = self.height)
        self.pButton = tk.Button(self, command = self.loadFile)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)

        #self.pack_propagate(1)
        #self.grid_propagate(1)

        self.pFileImage = Image.open("assets/folder.png")
        self.pFile = None #This should be the selected file.
        self.strFileName = ""

        self.pCallFunc = None #This should be a method, it is called when a new file is selected.


    def renderWidget(self):
        self.update()
        intHeight = self.winfo_height()
        self.updateImage(intHeight)

        print(self.width)

        intWidth = self.width - (intHeight + 10)

        self.pEntry.place(anchor = "w", rely = .5, width = intWidth)
        self.pButton.place(x = intWidth, width = intHeight, height = intHeight)

        self.update()

    def updateImage(self, intHeight):
        self.update()

        pFolderImage = Image.open("assets/folder.png")
        pFolderImage = pFolderImage.resize((intHeight, intHeight))
        self.pButtonImage = self.compileImage(pFolderImage)

        self.pButton.config(image = self.pButtonImage)

    def updateEntry(self, strFilename):
        """
        strFilename: Self explanatory.
        """

        self.pEntryTextVar.set(strFilename)

    def loadFile(self):
        pFile = filedialog.askopenfile("r", title = self.strFileTitle, filetypes = self.rFiles)

        if pFile:
            self.pFile = pFile
            self.strFileName = fileName(pFile.name)

            self.pEntryTextVar.set(self.strFileName)

            try:
                self.pCallFunc(self.pFile.name)

            except TypeError:
                pass

            print(self.strFileName)
        return

    def clearFile(self):
        self.pEntryTextVar.set("")

    def getEntry(self):
        return self.pEntry

    def getFile(self):
        return self.pFile

    def getFileName(self):
        return self.strFileName

    def grid(self, *args, **kvars):
        super().grid(*args, **kvars)
        self.renderWidget()

    def pack(self, *args, **kvars):
        super().pack(*args, **kvars)
        self.renderWidget()

    def place(self, *args, **kvars):
        super().place(*args, **kvars)
        self.renderWidget()

    def bind(self, sequence=None, func=None, add=None):
        if sequence == "<FileSelected>": #We want to add another event to allow for updating when a new file is selected.
            self.pCallFunc = func
            return

        super().bind(sequence, func, add)
        return

    def compileImage(self, pImage):
        pImage = ImageTk.PhotoImage(pImage)
        return pImage

if __name__ == "__main__":

    pWindow = tk.Tk()

    pFrame = FileLoader(pWindow, strFileTitle = "Open Image")
    pFrame.pack(fill = "both", expand = True)

    print(pFrame.winfo_width())

    pWindow.mainloop()
