'''
Created on Jul 19, 2020

@author: Zach Wallace (BP)

    Holds the code that displays an instance of a map.
'''

import tkinter as tk
from CustomMapCompiler import ExportMap
from libraries.gui.thumbnailViewer import ThumbnailViewer
from libraries.gui.loadFile import FileLoader
from libraries.map import GameMap

from math import floor
from setuptools.command.easy_install import PthDistributions

class MapScreen(tk.Frame):

    def __init__(self, master, load= None, *args, **kvargs): #Load is used when you want to add an existing bns.
        """
        master: The parent to this tk.Frame
        load: A GameMap instance.
        """

        self.font = ("Source Code Pro", 10)

        self.pNameVar = tk.StringVar()
        self.pCommentVar = tk.StringVar()
        self.pCheckBoxVar = tk.BooleanVar()

        if load:
            self.pMapData = load
            self.bLoadedMap = True
        else:
            self.pMapData = GameMap()
            self.bLoadedMap = False

        super().__init__(master, *args, **kvargs)

        self.pack_propagate(0)
        self.grid_propagate(0)

    def renderWidgets(self):

        self.update()

        width = self.winfo_width()
        loadWidth = floor(width / 2 - 20)
        textWidth = floor(loadWidth/self.font[1])

        self.pThumbnail = ThumbnailViewer(self, width = floor(width / 2), bd = 2, relief = "sunken")

        self.pDetailsFrame = tk.Frame(self, bd = 0, padx = 0, pady = 0)
        pNameTitle = tk.Label(self.pDetailsFrame, text= "Map Name:", font = self.font, anchor = "w", justify = "left")
        self.pNameInput = tk.Entry(self.pDetailsFrame, font = self.font, width = textWidth, textvariable = self.pNameVar)
        pMapTitle = tk.Label(self.pDetailsFrame, text= "Map File:", font = self.font, anchor = "w", justify = "left")
        self.pMapInput = FileLoader(self.pDetailsFrame, [("Valve Map File", ".bsp")], "Select Map File", self.font, width= loadWidth)
        pThumbnailTitle = tk.Label(self.pDetailsFrame, text= "Thumbnail:", font = self.font, anchor = "w", justify = "left")
        self.pThumbnailInput = FileLoader(self.pDetailsFrame, strFileTitle= "Select Thumbnail File", font = self.font, width= loadWidth)
        pCommentTitle = tk.Label(self.pDetailsFrame, text = "Comment:", font = self.font, anchor = "w", justify = "left")
        self.pCommentInput = tk.Entry(self.pDetailsFrame, width = textWidth, font = self.font, textvariable = self.pCommentVar)
        #pLockTitle = tk.Label(self.pDetailsFrame, "Lock By Default:", font = self.font, anchor = "w", justify = "left")
        self.pLockInput = tk.Checkbutton(self.pDetailsFrame, text = "Lock By Default", font = self.font, onvalue = True, offvalue = False, variable = self.pCheckBoxVar, anchor = "w", padx = 0, pady = 10)
        self.pExportButton = tk.Button(self.pDetailsFrame, text = "Export", font = self.font, command = self.exportMap)


        self.pThumbnail.place(relx = 0.01, rely = 0.01)
        self.pDetailsFrame.place(relx = 0.52, rely = 0.01)
        pNameTitle.pack(fill = "both")
        self.pNameInput.pack(fill = "both")
        pMapTitle.pack(fill = "both")
        self.pMapInput.pack(fill = "both")
        pThumbnailTitle.pack(fill = "both")
        self.pThumbnailInput.pack(fill = "both")
        pCommentTitle.pack(fill = "both")
        self.pCommentInput.pack(fill = "both")
        self.pLockInput.pack(fill = "both")
        self.pExportButton.pack(anchor = "w")

        #Bindings
        self.pMapInput.getEntry().bind("<Button-1>", self.clearMap)
        self.pThumbnailInput.getEntry().bind("<Button-1>", self.clearImage)
        self.pThumbnailInput.bind("<FileSelected>", self.updateImage)

        if self.bLoadedMap:
            self.pThumbnail.setImage(self.pMapData.getImage())

            self.pNameInput.config(text = self.pMapData.getName())
            self.pMapInput.config(text = self.pMapData.getMap())

        self.update()

        print(self.pCommentInput.winfo_height())

    def exportMap(self):
        self.pMapData.setName(self.pNameVar.get())
        self.pMapData.setMap(self.pMapInput.getFile().name)
        self.pMapData.setComment(self.pCommentVar.get())
        self.pMapData.setPILImage(self.pThumbnail.getImage())
        self.pMapData.setLocked(self.pCheckBoxVar.get())
        ExportMap(self.pMapData)

    def updateImage(self, strImagePath):
        """
        strImagePath: A file path, should be pointing to an image file!

        Called by an event from self.pThumbnailInput.
        """
        self.pThumbnail.setImage(strImagePath)
        return

    def clearMap(self, event):
        print("Clearing map")
        self.pMapInput.clearFile()

    def clearImage(self, event):
        print("Clearing Image")
        self.pThumbnailInput.clearFile()
        self.pThumbnail.resetImage()

    def pack(self, *args):
        super().pack(*args)
        self.renderWidgets()

    def grid(self, *args):
        super().grid(*args)
        self.renderWidgets()

    def place(self, *args):
        super().place(*args)
        self.renderWidgets()

if __name__ == "__main__":

    master = tk.Tk()

    screen = MapScreen(master, bg = "floral white")
    screen.pack()

    master.mainloop()
