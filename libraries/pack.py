'''
Created on Jul 19, 2020

@author: Zach Wallace (BP)

    Contains the data of a map pack instance.
'''

from PIL import Image
from libraries.bonusInstance import BonusInstance
from libraries.map import GameMap
from libraries import bnsParser

class GamePack(BonusInstance):

    def __init__(self, dictFolderInfo = {}):
        super().__init__(dictFolderInfo)
        self.rMaps = [] #GameMap Instances.

    """
        Override of compiling to remove the image tag.
    """
    def compileInstance(self):
        #Get the dictionary of compiling the folderinfo.
        dictPreComp = super().compileInstance()
        #Now remove the key "image".
        dictPreComp.pop("image", None)
        return dictPreComp

    def compileMaps(self):
        #Create the dictionary we will return.
        dictMaps = {}
        #Iterate through all maps and compile.
        for pMap in self.rMaps:
            #Merge the map data into the dictionary.
            dictMaps.update(pMap.compileInstance())

        return dictMaps

    """
        Adds in a map instance to this pack.

        pMap: GameMap instance
    """
    def addMap(self, pMap):
        pMap.enablePack()
        self.rMaps.append(pMap)
        return

    """
        Takes a dictionary and creates a map instance.
        It then appends to the pack.

        dictMap: A dictionary which contains the json .bns data of a map.
    """
    def importMap(self, dictMap):
        self.addMap(GameMap(dictMap, True))

    """
        Takes a dictionary and creates map instances.

        dictMaps: A dictionary which conains the json .bns data of maps.
    """
    def importMaps(self, dictMaps):
        """
        rMaps: An array, which contains un-instanced maps.

        This method will also work with a single map in an array.
        """
        for map, keyvals in dictMaps.items():
            self.addMap(GameMap({map: keyvals}, True))

    """
        Prints the data about all maps within this pack.
    """
    def printMaps(self):
        for pMap in self.rMaps:
            print(pMap.compileInstance())

    def getMaps(self):
        return self.rMaps

if __name__ == "__main__":
    pass
