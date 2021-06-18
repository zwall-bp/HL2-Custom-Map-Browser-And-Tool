'''
Created on Jul 19, 2020

@author: crusty-cast
'''

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
from math import floor
import os
import random

from libraries.gui.mapScreen import MapScreen

class EditorScreen(tk.Tk):

    """
        Must allow to create tabs to cycle through different maps.
        Must also house the map or pack screen.
    """

    def __init__(self):
        super().__init__()

        self.aspectRatio = 16/6
        self.width = floor(self.winfo_screenwidth() / 2)
        self.height = floor(self.width / self.aspectRatio)

        self.pTabControl = ttk.Notebook(self)
        self.rTabs = []

        self.resizable(False, False)
        self.geometry(f"{self.width}x{self.height}")

        self.pNewTab = tk.Frame(self.pTabControl)

        self.renderScene()

        self.update()

        self.mainloop()

    def renderScene(self):
        self.addTab()

    def addTab(self, dictData = None):
        """
        Create a MapScreen instance, and add it to the tabs.
        """
        pMapScreen = MapScreen(self.pTabControl)

        self.rTabs.append(pMapScreen)

        self.pTabControl.pack(expand = True, fill = "both")
        self.pTabControl.add(pMapScreen, text = "New Map")
        pMapScreen.renderWidgets()

    def removeTab(self):
        pass

if __name__ == "__main__":
    print("Never use this to test! It needs to be ran by a script which has access to the assets/ directory!")
