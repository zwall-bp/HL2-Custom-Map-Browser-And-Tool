'''
Created on Jul 19, 2020

@author: Zach Wallace (BP)

A class which represents a single map entry within a .bns file.

Maps can contain:
    Map File
    Thumbnail
    Comment
'''

from PIL import Image
from libraries.bonusInstance import BonusInstance
from libraries import bnsParser

class GameMap(BonusInstance):

    def __init__(self, dictData = {}, bInPack = False):
        """
            Map attributes:
            map: The path to the map file.
        """
        super().__init__(dictData)
        if bInPack:
            self.setData("packed", True)

    #Flag this map as in a pack.
    def enablePack(self):
        self.setData("packed", True)

    #Remove pack flag
    def disablePack(self):
        seld.setData("packed", False)

    def inPack(self):
        return self.getData("packed")

    def setMap(self, strMapPath):
        self.setData("map", strMapPath)
        return

    def getMap(self):
        return self.getData("map")

if __name__ == "__main__":
    pass
