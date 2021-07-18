"""
Created on Jun 16, 2020

@author: Zach Wallace (BP)

An abstract class representing an instance in the bonus map page.

Used for both a Map instance and Pack instance.
"""

from PIL import Image
from math import floor, ceil
from libraries import bnsParser

class BonusInstance():
    '''
    classdocs
    '''


    def __init__(self, dictData = {}):
        """
            Shared attributes:
            name: Name of the map/pack.
            comment: A comment about the map/pack.
            thumbnail: The path to a .tga image.
            lock: Is the map/pack locked by default.
        """

        self.dictData = {}

        #The keys in the dict are the name value.
        if(len(dictData)):
            #There is a key.
            self.dictData["name"] = list(dictData.keys())[0]
            #Iterate through the first key.
            for key, val in dictData[self.dictData["name"]].items():
                self.dictData[key] = val

        #PIL instance.
        #An alternative a premade thumbnail.
        self.pImage = None
        self.bThumbnailed = False
        self.bUsePIL = False

    def compileInstance(self):
        """
        Returns a dictionary.

        Turn all of this instance's data into a dictionary.
        """
        #Check to see if we can export.
        if not self.validateExport():
            #Can't export!
            return
        #Create a dictionary which will hold all of the keyvals.
        dictKeyvals = {}
        #Iterate over all of the dictData putting all inside of the keyvals.
        for key, val in self.dictData.items():
            #Skip over the name.
            if key == "name":
                continue
            dictKeyvals[key] = val
        #Now return a dictionary with the key being the name of the map.
        return {self.getName(): dictKeyvals}

    """
    Checks to see if the instance has a name, in order to export correctly.
    """
    def validateExport(self):
        return bool(self.getName())

    """
    Saves a TGA file of pImage.

    Used when PIL is behind the creation of the image.

    strPath: File's output path and name.
    """
    def compileCustomImage(self, strPath):
        #Check to make sure we have a PIL instance.
        if self.bUsePIL:
            #Check to see if the image has already been thumbnailed.
            if self.bThumbnailed:
                self.pImage.save(strPath, format="tga")
                return

            #Now, crop it, just in case.
            nWidth = self.pImage.width
            nHeight = self.pImage.height
            #Scale down, with the lesser resolution deciding the clamp.
            if nWidth < nHeight:
                #Width is smaller, clamp to that.
                flScale = 180 / nWidth
                nWidth = 180
                nHeight = max(ceil(nHeight * flScale), 100)
            else:
                #Height is smaller, clamp to that.
                flScale = 100 / nHeight
                nHeight = 100
                nWidth = max(ceil(nWidth * flScale), 180)
            #Now scale down the image to the new width/height.
            #Move the resized to the current image.
            pResized = self.pImage.resize((nWidth, nHeight), Image.LANCZOS)
            self.pImage.close()
            self.pImage = pResized
            #Crop out all of the fat.
            pCropped = self.pImage.crop((0, 0, 180, 100))
            self.pImage.close()
            self.pImage = pCropped

            #It's impossible to expand an image. So, we will instead be creating a new image
            #And superimpose the thumbnail onto this.
            pBackground = Image.new("RGBA", (256, 128), color=(0, 0, 0, 0))
            pBackground.paste(self.pImage)
            #We are finished with the original image.
            self.pImage.close()

            #We now save the image to the given path.
            pBackground.save(strPath, format="TGA")
            #Move our current image back into pImage.
            self.pImage = pBackground
            self.bThumbnailed = True

            #Complete this by setting the thumbnail value to this path.
            self.setThumbnail(strPath)
            return

    """
    Enables and loads an image into a PIL instance.

    strPath: Path to image file.
    """
    def loadPILImage(self, strPath: str):
        #Check if there is already an image loaded.
        if self.pImage:
            #Close it.
            self.pImage.close()

        #Load in the new image.
        self.pImage = Image.open(strPath)
        self.bUsePIL = True

    """
    Enables and sets an image as the PIL instance.

    pImage: PIL Image instance.
    """
    def setPILImage(self, pImage: Image):
        #Check if there is already an image loaded.
        if self.pImage:
            #Close it.
            self.pImage.close()

        #Load in the new image.
        self.pImage = pImage
        self.bUsePIL = True
        #Clear Thumbnail
        if self.bThumbnailed:
            self.bThumbnailed = False

    """
    Disables the use of the PIL image.
    """
    def disablePILImage(self):
        #Check to make sure pImage has loaded an image.
        if self.pImage:
            #Close the file.
            self.pImage.close()

        self.bUsePIL = False

    #Sets a key to the value.
    def setData(self, strKey: str, strVal: str):
        self.dictData[strKey] = strVal
        return

    #Attempts to get a key. If it doesn't exist, returns None.
    def getData(self, strKey: str):
        return self.dictData.get(strKey, None)

    def getAllData(self):
        return self.dictData

    def setName(self, strName):
        self.setData("name", strName)
        return

    def setComment(self, strComment):
        self.setData("comment", strComment)
        return

    def setLocked(self, bLock: bool):
        if bLock:
            self.setData("lock", "1")
        else:
            self.setData("lock", "0")

    def setThumbnail(self, strImageDir):
        self.setData("image", strImageDir)

    def setThumbnailXOffset(self, X: int):
        self.setData("imageX", X)

    def setThumbnailYOffset(self, Y: int):
        self.setData("imageY", Y)

    def setThumbnailOffset(self, X: int, Y: int):
        self.setData("imageX", X)
        self.setData("imageY", Y)

    def setThumbnailScale(self, flScale: float):
        self.setData("imageScale", round(flScale, 3))

    def getName(self):
        return self.getData("name")

    def getComment(self):
        return self.getData("comment")

    def isLocked(self):
        strLock = self.getData("lock")
        if strLock == "1":
            return True
        return False

    def getThumbnail(self):
        return self.getData("image")

    def getThumbnailXOffset(self):
        return self.getData("imageX")

    def getThumbnailYOffset(self):
        return self.getData("imageY")

    def getThumbnailScale(self):
        return self.getData("imageScale")

    def getThumbnailOffset(self):
        return (self.getThumbnailXOffset(), self.getThumbnailYOffset())

    def usingPIL(self):
        return self.bUsePIL

    def hasImage(self):
        if self.bUsePIL:
            if self.pImage:
                return True
            return False
        return bool(self.getThumbnail())

if __name__ == "__main__":
    pass
