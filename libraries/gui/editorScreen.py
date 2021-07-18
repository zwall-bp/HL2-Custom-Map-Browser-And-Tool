'''
Created on Jul 19, 2020

@author: Zach Wallace
'''

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
from math import floor
import json as js
import os
import random

from libraries.gui.mapScreen import MapScreen
from libraries.gui.packScreen import PackScreen
from libraries.gui.aboutScreen import AboutScreen
from libraries.map import GameMap
from libraries.pack import GamePack

class EditorScreen(tk.Tk):

    """
        Must allow to create tabs to cycle through different maps.
        Must also house the map or pack screen.
    """

    def __init__(self):
        super().__init__()

        #Set the title
        self.title("Custom Map Compiler")

        #Setting up a pack
        self.pPack = GamePack()

        self.aspectRatio = 16/6
        self.width = floor(self.winfo_screenwidth() / 2)
        self.height = floor(self.width / self.aspectRatio)
        #Map Stuff
        self.pMenu = tk.Menu(self)
        self.pMenuMap = tk.Menu(self.pMenu, tearoff=0)
        self.pMenuMap.add_command(label= "New Map", command=self.onAdd)
        self.pMenuMap.add_command(label= "Close Map", command=self.onClose)
        self.pMenuMap.add_separator()
        self.pMenuMap.add_command(label= "Export", command=self.ExportMap)
        self.pMenuMap.add_separator()
        self.pMenuMap.add_command(label= "Save Map", command=self.SaveMap)
        self.pMenuMap.add_command(label= "Load Map", command=self.LoadMap)
        self.pMenuMap.add_separator()
        self.pMenuMap.add_command(label= "Exit", command=self.quit)

        self.pMenu.add_cascade(label= "Map", menu= self.pMenuMap)
        #Map Pack Stuff
        self.pMenuPack = tk.Menu(self.pMenu, tearoff=0)

        self.pPackEnabled = tk.BooleanVar()
        self.pMenuPack.add_checkbutton(label= "Map Pack", command=self.updatePack, variable=self.pPackEnabled, onvalue=True, offvalue=False)
        self.pMenuPack.add_separator()
        self.pMenuPack.add_command(label= "Export", command=self.ExportPack)
        self.pMenuPack.add_separator()
        self.pMenuPack.add_command(label="Move Left", command=self.onMoveLeft)
        self.pMenuPack.add_command(label="Move Right", command=self.onMoveRight)
        self.pMenuPack.add_separator()
        self.pMenuPack.add_command(label= "Save Pack", command=self.savePack)
        self.pMenuPack.add_command(label= "Load Pack", command=self.loadPack)

        self.pMenu.add_cascade(label= "Pack", menu= self.pMenuPack)

        #self.pMenuHelp = tk.Menu(self.pMenu, tearoff=0)
        #self.pMenuHelp.add_command(label="About", command=self.openAbout)

        #self.pMenu.add_cascade(label= "Help", menu= self.pMenuHelp)

        self.config(menu=self.pMenu)

        self.pTabControl = ttk.Notebook(self)
        self.pTabControl.enable_traversal()

        self.resizable(False, False)
        self.geometry(f"{self.width}x{self.height}")

        self.pNewTab = tk.Frame(self.pTabControl)

        self.renderScene()
        #Disable the map/pack stuff at the beginning.
        self.disableMapOptions()
        self.disablePackOptions()
        #Create events
        self.pTabControl.bind("<<NotebookTabChanged>>", self.updateOptions)

        self.update()

        self.mainloop()

    def renderScene(self):
        self.pTabControl.pack(expand = True, fill = "both")

    def addTab(self, pMap = None):
        """
        Create a MapScreen instance, and add it to the tabs.
        """
        pMapScreen = MapScreen(self.pTabControl, pMap)

        #Display the name of the map instead of "New Map"
        if pMap:
            self.pTabControl.add(pMapScreen, text = list(pMap.getName()))
        else:
            self.pTabControl.add(pMapScreen, text = "New Map")
        #Set up the binding to change the text of the tab from the editor.
        pMapScreen.bindTitleToTab(self.pTabControl, self.pTabControl.tabs()[-1])
        #Move to the new tab to finish setup.
        self.pTabControl.select(self.pTabControl.tabs()[-1])

        pMapScreen.renderWidgets()

    """
    Removes a tab instance.
    """
    def closeTab(self, strTab = None):
        if not strTab:
            strTab = self.pTabControl.select()
            if not strTab:
                #No tab open
                return
        pMapScreen = self.nametowidget(strTab)
        self.pTabControl.forget(strTab)
        pMapScreen.destroy()

    """
    Checks pPackEnabled to see if we should enable or disable it.
    """
    def updatePack(self):
        #Check to see if we should enable it.
        if(self.pPackEnabled.get()):
            #Should be enabled.
            self.enablePack()
            return
        #Should be disabled.
        self.disablePack()
        return

    """
    Adds a tab to the front, and sets it to the pack.
    """
    def enablePack(self):
        #Create a new PackScreen instance.
        pPackScreen = PackScreen(self.pTabControl, self.pPack)

        strPackName = "New Pack"

        #Display the name of the pack instead of "New Pack (P)"
        if self.pPack.getName():
            strPackName = self.pPack.getName()

        #Change the way we add it if there are('nt) tabs.
        if len(self.pTabControl.tabs()) > 0:
            self.pTabControl.insert(self.pTabControl.tabs()[0], pPackScreen, text = strPackName + " (P)")
        else:
            self.pTabControl.add(pPackScreen, text = strPackName + " (P)")
        self.title("Custom Map Compiler: " + strPackName)

        #Set up the binding to change the text of the tab from the editor.
        pPackScreen.bindTitleToTab(self.title, self.pTabControl, self.pTabControl.tabs()[0])
        #Move to the new tab to finish setup.
        self.pTabControl.select(self.pTabControl.tabs()[0])

        pPackScreen.renderWidgets()


    """
    Removes the front tab if it's a pack.
    """
    def disablePack(self):
        strPack = self.pTabControl.tabs()[0]
        pPackScreen = self.nametowidget(strPack)
        self.pTabControl.forget(pPackScreen)
        pPackScreen.updatePack()
        pPackScreen.destroy()
        self.title("Custom Map Compiler")

    """
    Enables options exclusive to Packs
    """
    def enablePackOptions(self):
        #Export
        self.pMenuPack.entryconfigure(2, state="active")
        #Save
        self.pMenuPack.entryconfigure(7, state="active")

    """
    Disables options exclusive to Packs
    """
    def disablePackOptions(self):
        #Export
        self.pMenuPack.entryconfigure(2, state="disabled")
        #Save
        self.pMenuPack.entryconfigure(7, state="disabled")

    """
    Enable options exlcusive to Maps
    """
    def enableMapOptions(self):
        #Close Map
        self.pMenuMap.entryconfigure(1, state="active")
        #Export
        self.pMenuMap.entryconfigure(3, state="active")
        #Save
        self.pMenuMap.entryconfigure(5, state="active")

    """
    Disable options exclusive to Maps
    """
    def disableMapOptions(self):
        #Close Map
        self.pMenuMap.entryconfigure(1, state="disabled")
        #Export
        self.pMenuMap.entryconfigure(3, state="disabled")
        #Save/Load
        self.pMenuMap.entryconfigure(5, state="disabled")

    """
    Checks to see if the current selected tab is the pack.
    """
    def packSelected(self):
        if not self.pPackEnabled.get():
            #Pack isn't enabled to begin with.
            return False
        #Returns true if we are at index 0, false if we are on anything else.
        return self.pTabControl.index(self.pTabControl.select()) == 0

    """
    Checks to see if the current tab is the pack.
    And if it is the pack, raise a window.
    """
    def assertPack(self):
        if self.packSelected():
            messagebox.showerror("Pack Selected", "Can't export a pack as a map.")
            return True
        else:
            return False

    """
    Gets an array of tab instances of all the maps.
    Different method for when there is a pack tab.
    """
    def getMapTabs(self):
        if self.pPackEnabled.get():
            #Remove first instance, it's the pack.
            return self.pTabControl.tabs()[1:]
        #All tabs are maps.
        return self.pTabControl.tabs()

    """
    Moves a map tab to the left.
    """
    def onMoveLeft(self):
        self.moveTab(self.pTabControl.select(), False)

    """
    Moves a map tab to the right.
    """
    def onMoveRight(self):
        self.moveTab(self.pTabControl.select(), True)

    """
    Moves the given tab.
    bRight: True, to the right. False, to the left.
    """
    def moveTab(self, strTabName, bRight):
        #Check to make sure there's enough tabs to move.
        nTabs = len(self.pTabControl.tabs())
        if nTabs < 2:
            return
        #Get index of the given tab
        nTabIdx = self.pTabControl.tabs().index(strTabName)
        #Check to see if it doesn't exist.
        if nTabIdx == -1:
            #It doesn't, do nothing.
            return
        elif self.pPackEnabled.get() and nTabIdx == 0:
            #User is trying to move the pack.
            return
        #Tab is somewhere in the middle, move it.
        pMovingTab = self.nametowidget(strTabName)
        if bRight:
            #Moving to the right.
            if nTabIdx == nTabs - 1:
                return
            #Check to see if we are moving to the end.
            if nTabIdx == nTabs - 2:
                self.pTabControl.insert("end", pMovingTab)
                return
            self.pTabControl.insert(self.pTabControl.index(nTabIdx + 1), pMovingTab)
        else:
            #Check to make sure it's not already at the end.
            if nTabIdx == 0:
                return
            #Check to see if we shouldn't move to the left of the pack screen.
            elif self.pPackEnabled.get() and nTabIdx == 1:
                return
            self.pTabControl.insert(self.pTabControl.index(nTabIdx - 1), pMovingTab)

    """
    File IO
    """

    """
    Exports a map instance to a project.
    """
    def ExportMap(self):
        #Get the widget we are trying to export.
        strTab = self.pTabControl.select()
        if not strTab:
            messagebox.showerror("No Map!", "There isn't a map project open to export!")
            return
        pMapScreen = self.nametowidget(self.pTabControl.select())
        pMapScreen.exportMap()

    """
    Exports a pack instance to a project.
    """
    def ExportPack(self):
        #Iterate over every map file, and add it to the pack's maps.
        self.pPack.clearMaps()
        for strMapID in self.getMapTabs():
            pMapScreen = self.nametowidget(strMapID)
            #When we get the map, it will set up the PIL image correctly, so we can easily export from here.
            pMap = self.nametowidget(pMapScreen).getGameMap()
            if not pMap.validateExport():
                #Map isn't valid, go to it and raise an error.
                self.pTabControl.select(strMapID)
                messagebox.showerror("Incomplete Map", "Please provide your map with a name and map file.")
                return
            self.pPack.addMap(pMap)
        #Now, export.
        pPackScreen = self.nametowidget(self.pTabControl.tabs()[0])
        pPackScreen.exportPack()


    """
    Creates a .json file with the current map
    """
    def SaveMap(self):
        if self.assertPack():
            return
        #Get the widget we are trying to export.
        strTab = self.pTabControl.select()
        if not strTab:
            messagebox.showerror("No Map!", "There isn't a map project open to save!")
            return
        #Get the widget we are trying to save.
        pMapScreen = self.nametowidget(strTab)
        #Get the file path to where we will save the json.
        strSaveFile = filedialog.asksaveasfilename(title="Save current map data to .json", filetypes=[("Javascript Object Notation", ".json")])
        if not strSaveFile:
            #User canceled.
            return
        #Now save the data.
        pMapScreen.saveMap(strSaveFile)

    """
    Opens a file dialog and asks the user to open a .json file of a map.
    """
    def LoadMap(self):
        #Get the json of the map(s) we are wanting to load.
        dictMaps = None
        file = filedialog.askopenfile("r", title= "Open a .json with map data", filetypes=[("Javascript Object Notation", ".json")])
        #Check to see if there was nothing selected.
        if not file:
            return
        #File Selected.
        dictMaps = js.load(file)
        file.close()
        #Iterate over each map.
        for name, keyvals in dictMaps.items():
            self.addTab(GameMap({name: keyvals}))


    """
    Creates a .json file with a pack and the maps associated with it.
    """
    def savePack(self):
        #Get the Map Screen.
        pPackScreen = self.nametowidget(self.pTabControl.tabs()[0])
        #Clear everything in the pack.
        self.pPack.clearMaps()
        #Iterate through each map, getting all of the GameMap instances
        for strMapScreen in self.getMapTabs():
            pMapScreen = self.nametowidget(strMapScreen)
            self.pPack.addMap(pMapScreen.getGameMap())
        #Get the file path to where we will save the json.
        strSaveFile = filedialog.asksaveasfilename(title="Save current pack data to .json", filetypes=[("Javascript Object Notation", ".json")])
        if not strSaveFile:
            #User canceled.
            return
        #Now to save the pack.
        pPackScreen.savePack(strSaveFile)

    """
    Opens a file dialog and asks the user to open a .json file of a pack.
    """
    def loadPack(self):
        #Get the json of the pack we are wanting to load.
        dictPack = None
        file = filedialog.askopenfile("r", title= "Open a .json with map data", filetypes=[("Javascript Object Notation", ".json")])
        #Check to see if there was nothing selected.
        if not file:
            return
        dictPack = js.load(file)
        file.close()
        #Clear absolutely everything.
        self.clearAllTabs()
        #Pop out the maps first.
        dictMaps = dictPack.pop("maps", None)
        #Change pPack to a new Pack instance.
        self.pPack = GamePack(dictPack)
        #Enable the Pack
        self.pPackEnabled.set(True)
        self.enablePack()
        #Iterate over each map.
        for name, keyvals in dictMaps.items():
            self.addTab(GameMap({name: keyvals}))


    """
    Clears all of the tabs
    """
    def clearAllTabs(self):
        #Make sure we remove the pack tab.
        self.pPackEnabled.set(False)
        #Iterate over every tab, removing them.
        for strScreenName in self.pTabControl.tabs():
            self.closeTab(strScreenName)
    """
    Bindings
    """

    """
    Updates the available options by disabling some, and enabling others.
    """
    def updateOptions(self, eventdata):
        if self.packSelected():
            #We are looking at a pack
            self.enablePackOptions()
            self.disableMapOptions()
            return
        #We are looking at a map.
        self.enableMapOptions()
        self.disablePackOptions()
        return

    """
    Binding for Add Map on menu.
    """
    def onAdd(self):
        self.addTab()

    """
    Binding for Close Map on menu.
    """
    def onClose(self):
        self.closeTab()

    def removeTab(self):
        pass

    """
    Open the about page.
    """
    def openAbout(self):
        pAbout = AboutScreen(self)
        return

if __name__ == "__main__":
    print("Never use this to test! It needs to be ran by a script which has access to the assets/ directory!")
