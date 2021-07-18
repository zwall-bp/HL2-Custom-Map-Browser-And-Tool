'''
Created on Jul 19, 2020

@author: Zach Wallace (BP)

    Holds the code that displays an instance of a map.
'''

import tkinter as tk
from tkinter import messagebox
from libraries.compiler import ExportMap, SaveData, GetCleanName
from libraries.gui.thumbnailViewer import ThumbnailViewer
from libraries.gui.loadFile import FileLoader
from libraries.map import GameMap

from math import floor

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

        self.pTab = None #Pointer to the tab manager tab.
        self.strTabName = None #Name of the tab.

        if load:
            self.pMapData = load
            self.bLoadedMap = True
        else:
            self.pMapData = GameMap()
            self.bLoadedMap = False

        super().__init__(master, *args, **kvargs)

        self.pack_propagate(0)
        self.grid_propagate(0)

    def __del__(self):
        print("Map Screen has been deleted!")

    def renderWidgets(self):

        self.update()

        width = self.winfo_width()
        loadWidth = floor(width / 2 - 10)
        textWidth = floor(loadWidth/self.font[1])

        """
            All widgets in the screen.
        """

        self.pThumbnail = ThumbnailViewer(
            self,
            width = floor(width / 2) - 5,
            bd = 2,
            relief = "sunken"
        )
        self.pDetailsFrame = tk.Frame(
            self,
            bd = 0,
            padx = 0,
            pady = 0,
        )
        pNameTitle = tk.Label(
            self.pDetailsFrame,
            text= "Map Name:",
            font = self.font,
            anchor = "w",
            justify = "left"
        )
        self.pNameInput = tk.Entry(
            self.pDetailsFrame,
            font = self.font,
            width = textWidth,
            textvariable = self.pNameVar
        )
        pMapTitle = tk.Label(
            self.pDetailsFrame,
            text= "Map File:",
            font = self.font,
            anchor = "w",
            justify = "left"
        )
        self.pMapInput = FileLoader(
            self.pDetailsFrame,
            [("Valve Map File", ".bsp")],
            "Select Map File",
            self.font,
            width= loadWidth
        )
        pThumbnailTitle = tk.Label(
            self.pDetailsFrame,
            text= "Thumbnail:",
            font = self.font,
            anchor = "w",
            justify = "left"
        )
        self.pThumbnailInput = FileLoader(
            self.pDetailsFrame,
            strFileTitle= "Select Thumbnail File",
            font = self.font,
            width= loadWidth
        )
        pCommentTitle = tk.Label(
            self.pDetailsFrame,
            text = "Comment:",
            font = self.font,
            anchor = "w",
            justify = "left"
        )
        self.pCommentInput = tk.Entry(
            self.pDetailsFrame,
            width = textWidth,
            font = self.font,
            textvariable = self.pCommentVar
        )
        self.pLockInput = tk.Checkbutton(
            self.pDetailsFrame,
            text = "Lock By Default",
            font = self.font,
            onvalue = True,
            offvalue = False,
            variable = self.pCheckBoxVar,
            anchor = "w",
            padx = 0,
            pady = 10
        )

        self.pThumbnail.place(relx = 0.005, rely = 0.01)
        self.pDetailsFrame.place(relx = 0.51, rely = 0.01)
        pNameTitle.pack(fill = "both")
        self.pNameInput.pack(fill = "both")
        pMapTitle.pack(fill = "both")
        self.pMapInput.pack(fill = "both")
        pThumbnailTitle.pack(fill = "both")
        self.pThumbnailInput.pack(fill = "both")
        pCommentTitle.pack(fill = "both")
        self.pCommentInput.pack(fill = "both")
        self.pLockInput.pack(fill = "both")


        #Bindings
        self.pMapInput.getEntry().bind("<Button-1>", self.clearMap)
        self.pThumbnailInput.getEntry().bind("<Button-1>", self.clearImage)
        self.pThumbnailInput.bind("<FileSelected>", self.updateImage)

        #Setting up a loaded map.
        if self.bLoadedMap:
            self.pNameVar.set(self.pMapData.getName())
            self.pCommentVar.set(self.pMapData.getComment())
            self.pCheckBoxVar.set(self.pMapData.isLocked())
            self.pMapInput.setFile(self.pMapData.getMap())
            if not None in self.pMapData.getThumbnailOffset() or self.pMapData.getThumbnailScale():
                #Add a binding.
                self.bind("<<ThumbnailNewImage>>", self.onImageLoaded)
            self.pThumbnailInput.setFile(self.pMapData.getThumbnail())

        self.update()

    """
    Update the image scale/position.
    """
    def onImageLoaded(self, event):
        tuPos = self.pMapData.getThumbnailOffset()
        flScale = self.pMapData.getThumbnailScale()
        if flScale:
            self.pThumbnail.setScale(flScale)
        if not None in tuPos:
            self.pThumbnail.moveImage(tuPos[0], tuPos[1])
            self.pThumbnail.tuImagePos = tuPos
        self.unbind("<<ThumbnailNewImage>>")

    """
    Creates a bind on pNameVar to change the title of a tab.
    """
    def bindTitleToTab(self, pTab, strTabName):
        self.pTab = pTab
        self.strTabName = strTabName
        self.pNameVar.trace("w", self.updateTab)

    """
    Fired every time the title is updated.
    """
    def updateTab(self, *args):
        #Check to see if it's blank.
        if self.pNameVar.get():
            #There is something.
            self.pTab.tab(self.strTabName, text=self.pNameVar.get())
            return
        #There is nothing there
        self.pTab.tab(self.strTabName, text="New Map")

    """
    Updates all of pMapData with the Frame's Data.
    """
    def updateData(self):
        self.pMapData.setName(self.pNameVar.get())
        self.pMapData.setMap(self.pMapInput.getFilePath())
        self.pMapData.setComment(self.pCommentVar.get())
        self.pMapData.setLocked(self.pCheckBoxVar.get())
        pImage = self.pThumbnail.getImage()
        if pImage:
            #Custom Image
            tuPos = self.pThumbnail.getPos()
            self.pMapData.setPILImage(self.pThumbnail.getImage())
            self.pMapData.setThumbnail(self.pThumbnailInput.getFilePath())
            self.pMapData.setThumbnailOffset(tuPos[0], tuPos[1])
            self.pMapData.setThumbnailScale(self.pThumbnail.getScale())

    """
    Creates a project folder.
    """
    def exportMap(self):
        #Make sure the export is valid.
        if not self.validateExport():
            return
        #Check to make sure the name is legal.
        try:
            GetCleanName(self.pNameVar.get())
        except Exception:
            messagebox.showerror("Illegal name!", f"The name \"{self.pNameVar.get()}\" is illegal.\nPlease add an alphanumeric character!")
            return
        self.updateData()
        #Check to see if the directory exists.
        try:
            ExportMap(self.pMapData)
        except FileExistsError:
            #Projct already exists! Ask what the user wants to do.
            strDecision = messagebox.askyesno("Project Exists!", f"{self.pMapData.getName()} Already Exists!\nWould you like to clear and overwrite the data?")
            if not strDecision:
                pass
            #Force it
            ExportMap(self.pMapData, pForceExport = True)
        #Tell that it was successful.
        messagebox.showinfo("Success!", f"{self.pMapData.getName()} has successfuly exported!\nCheck exports/")
        return

    """
    Creates a json.
    """
    def saveMap(self, strFile):
        self.updateData()
        SaveData(self.pMapData, strFile)
        return

    """
    Updates the data inside of the Map instance and returns the data.
    """
    def getGameMap(self):
        self.updateData()
        return self.pMapData

    def updateImage(self, strImagePath):
        """
        strImagePath: A file path, should be pointing to an image file!

        Called by an event from self.pThumbnailInput.
        """
        self.pThumbnail.setImage(strImagePath)
        return

    def clearMap(self, event):
        #print("Clearing map")
        self.pMapInput.clearFile()

    def clearImage(self, event):
        #print("Clearing Image")
        self.pThumbnailInput.clearFile()
        self.pThumbnail.resetImage()

    """
    Checks to make sure it has enough data to export correctly.
    If not, it will show an error and return false.
    """
    def validateExport(self):
        if self.pNameVar.get() and self.pMapInput.getFilePath():
            #There is a name, and it's "clean" and it has a file path to a map.
            return True
        #There is something missing.
        messagebox.showerror("Incomplete Map", "Please provide your map with a name and map file.")
        return False

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
