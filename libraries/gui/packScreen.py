'''
Created on Jul 19, 2020

@author: Zach Wallace (BP)

    Holds the code that displays an instance of a map pack.
'''

import tkinter as tk
from tkinter import messagebox
from libraries.compiler import ExportPack, SaveData, GetCleanName
from libraries.gui.thumbnailViewer import ThumbnailViewer
from libraries.gui.loadFile import FileLoader
from libraries.pack import GamePack

from math import floor

class PackScreen(tk.Frame):

    def __init__(self, master, load= None, *args, **kvargs): #Load is used when you want to add an existing bns.
        """
        master: The parent to this tk.Frame
        load: A GamePack instance.
        """

        self.font = ("Source Code Pro", 10)

        self.pNameVar = tk.StringVar()
        self.pCommentVar = tk.StringVar()
        self.pCheckBoxVar = tk.BooleanVar()

        self.pTab = None #Pointer to the tab manager tab.
        self.strTabName = None #Name of the tab.

        if load:
            self.pPackData = load
            self.bLoadedPack = True
        else:
            self.pPackData = GamePack()
            self.bLoadedPack = False

        super().__init__(master, *args, **kvargs)

        self.pack_propagate(0)
        self.grid_propagate(0)

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
            strDefaultImage = "./assets/packDefault.tga",
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
            text= "Pack Name:",
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
        pThumbnailTitle.pack(fill = "both")
        self.pThumbnailInput.pack(fill = "both")
        pCommentTitle.pack(fill = "both")
        self.pCommentInput.pack(fill = "both")
        self.pLockInput.pack(fill = "both")


        #Bindings
        self.pThumbnailInput.getEntry().bind("<Button-1>", self.clearImage)
        self.pThumbnailInput.bind("<FileSelected>", self.updateImage)

        #Setting up a loaded map.
        if self.bLoadedPack:
            if not self.pPackData.getName():
                return
            self.pNameVar.set(self.pPackData.getName())
            self.pCommentVar.set(self.pPackData.getComment())
            self.pCheckBoxVar.set(self.pPackData.isLocked())
            if not None in self.pPackData.getThumbnailOffset() or self.pPackData.getThumbnailScale():
                #Add a binding.
                self.bind("<<ThumbnailNewImage>>", self.onImageLoaded)
            self.pThumbnailInput.setFile(self.pPackData.getThumbnail())

        self.update()

    """
    Update the image scale/position.
    """
    def onImageLoaded(self, event):
        tuPos = self.pPackData.getThumbnailOffset()
        flScale = self.pPackData.getThumbnailScale()
        if flScale:
            self.pThumbnail.setScale(flScale)
        if not None in tuPos:
            self.pThumbnail.moveImage(tuPos[0], tuPos[1])
            self.pThumbnail.tuImagePos = tuPos
        self.unbind("<<ThumbnailNewImage>>")

    """
    Creates a bind on pNameVar to change the title of the window.
    """
    def bindTitleToTab(self, pTKTitle, pTab, strTabName):
        self.pTKTitle = pTKTitle
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
            self.pTab.tab(self.strTabName, text=f"{self.pNameVar.get()} (P)")
            self.pTKTitle(f"Custom Map Compiler: {self.pNameVar.get()}")
            return
        #There is nothing there
        self.pTab.tab(self.strTabName, text="New Pack (P)")
        self.pTKTitle("Custom Map Compiler: New Pack")

    """
    Updates all of the data inside of the pack.
    """
    def updatePack(self):
        self.pPackData.setName(self.pNameVar.get())
        self.pPackData.setComment(self.pCommentVar.get())
        self.pPackData.setLocked(self.pCheckBoxVar.get())
        pImage = self.pThumbnail.getImage()
        if pImage:
            #Custom Image
            tuPos = self.pThumbnail.getPos()
            self.pPackData.setPILImage(self.pThumbnail.getImage())
            self.pPackData.setThumbnail(self.pThumbnailInput.getFilePath())
            self.pPackData.setThumbnailOffset(tuPos[0], tuPos[1])
            self.pPackData.setThumbnailScale(self.pThumbnail.getScale())

    """
    Creates a project folder.
    """
    def exportPack(self):
        #Check to make sure the name is legal.
        try:
            GetCleanName(self.pNameVar.get())
        except Exception:
            messagebox.showerror("Illegal name!", f"The name \"{self.pNameVar.get()}\" is illegal.\nPlease add an alphanumeric character!")
            return
        self.updatePack()
        #Check to see if the directory exists.
        try:
            ExportPack(self.pPackData)
        except FileExistsError:
            #Projct already exists! Ask what the user wants to do.
            strDecision = messagebox.askyesno("Project Exists!", f"{self.pPackData.getName()} Already Exists!\nWould you like to clear and overwrite the data?")
            if not strDecision:
                pass
            #Force it
            ExportPack(self.pPackData, pForceExport = True)
        #Tell that it was successful.
        messagebox.showinfo("Success!", f"{self.pPackData.getName()} has successfuly exported!")
        return

    """
    Creates a json.
    """
    def savePack(self, strFile):
        self.updatePack()
        SaveData(self.pPackData, strFile, True)
        return

    def getGamePack(self):
        self.updatePack()
        return self.pPackData

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
