"""
Author: Builderpro
File: C:/Users/Builderpro/eclipse-workspace/BonusMapCompiler/libraries/gui/thumbnailViewer.py
Reason: Allows the user to drag and drop an image, then allow the user to drag around the image and zoom with the scroll wheel.
        The displayed thumbnail can be outputted.
"""

import tkinter as tk
from PIL import Image, ImageTk
from math import floor

class ThumbnailViewer(tk.Label):

    def __init__(self, master, *args, **kwargs):

        kwargs["anchor"] = kwargs.get("anchor", "nw")
        kwargs["padx"] = kwargs.get("padx", 0)
        kwargs["pady"] = kwargs.get("pady", 0)
        kwargs["bd"] = kwargs.get("bd", 0)

        super().__init__(master, *args, **kwargs)

        self.master = master

        self.x = 0
        self.y = 0

        self.initGeometry(kwargs)

        self.setImage("./assets/mapDefault.png")
        self.bNoImage = True #Prevents the user from scaling mapDefault.tga

        #Event Related Stuff
        self.bMouseOver = False

        self.tuStartPos = None #Record the position of the mouse when it's first pressed down, in order to move the image relative to the pos.
        self.flImageScale = 1 #The scale of the image, floats round up on resolution.

        self.intOriginalWidth = self.pImage.width()
        self.intOriginalHeight = self.pImage.height()

        self.bind("<MouseWheel>", self.mouseScroll)
        #Linux mouse wheel
        self.bind("<Button-4>", self.mouseScroll)
        self.bind("<Button-5>", self.mouseScroll)
        self.bind("<B1-Motion>", self.mouseMoveImage)
        self.bind("<ButtonRelease-1>", self.mouseRelease)

    def initGeometry(self, kwargs):
        """
        kwargs: Pass the kwards in __init__!

        We must make sure that this widget is at a 9:5 aspect ratio!
        This widget is the preview for what the user will be getting!
        """

        flAspectRatio = 9/5

        self.width = kwargs.get("width", 180)
        self.height = kwargs.get("height", 100)

        flGivenAspectRatio = self.width / self.height

        if flGivenAspectRatio != flAspectRatio:
            #I'm going to make width fixed.
            #print("Need to fix up!")
            self.height = round(self.height * (flGivenAspectRatio / flAspectRatio))
            #print(f"New Geometry: ({self.width}, {self.height})")

        #print(f"Desired ratio: {flAspectRatio}\nCalculated Ratio{self.width/self.height}")
        super().config(width = self.width, height = self.height)
        return

    def getImage(self):
        if self.bNoImage:
            return None
        return self.pUsedImage.crop((self.tuImagePos[0], self.tuImagePos[1], self.tuImagePos[0] + self.width, self.tuImagePos[1] + self.height))

    #Removes the current image and puts back the placeholder.
    def resetImage(self):
        #Don't want to reset when there is none.
        if self.bNoImage:
            return
        self.setImage("./assets/mapDefault.png")
        self.bNoImage = True #Prevents the user from scaling mapDefault.tga

    def setImage(self, strImagePath):
        """
        Asks for the PATH to the image,
        NOT AN IMAGE INSTANCE.
        """

        self.pRawImage = Image.open(strImagePath)

        if self.pRawImage.width < self.winfo_width():
            pass

        flWidthRatio = self.width / self.pRawImage.width
        flHeightRatio = self.height / self.pRawImage.height

        print(f"Width: {flWidthRatio}, Height: {flHeightRatio}")

        if flWidthRatio > 1 or flHeightRatio > 1:
            if flWidthRatio > flHeightRatio:
                print("Resizing Image Width!")
                intWidth = floor(self.pRawImage.width * flWidthRatio)
                intHeight = floor(self.pRawImage.height * flWidthRatio)

                self.pRawImage = self.pRawImage.resize((intWidth, intHeight))
            else:
                print("Resizing Image Height!")
                intWidth = floor(self.pRawImage.width * flHeightRatio)
                intHeight = floor(self.pRawImage.height * flHeightRatio)

                self.pRawImage = self.pRawImage.resize((intWidth, intHeight))

        self.pUsedImage = self.pRawImage #We want to use this one, as resizing the original will ruin the quality, per resize.

        self.pImage = self.compileImage(self.pUsedImage)

        intMidX = floor((self.pImage.width() / 2) - (self.width / 2))
        intMidY = floor((self.pImage.height() / 2) - (self.height / 2))

        self.moveImage(intMidX, intMidY)
        self.tuImagePos = (intMidX, intMidY)
        self.flImageScale = 1
        self.intOriginalWidth = self.pImage.width()
        self.intOriginalHeight = self.pImage.height()

        self.bNoImage = False

        return


    def compileImage(self, pImage):
        """
        pImage: An Image instance.

        pImage will be converted to an ImageTk.
        """
        return ImageTk.PhotoImage(pImage)

    def mouseMoveImage(self, rEvent):
        """
        Called when the mouse clicks and drags over the widget.
        Moves the image inside of the frame.
        """

        if self.bNoImage:
            return

        if not self.tuStartPos:
            self.tuStartPos = (rEvent.x, rEvent.y)

        intDeltaX = self.tuStartPos[0] - rEvent.x
        intDeltaY = self.tuStartPos[1] - rEvent.y

        self.moveImage(self. tuImagePos[0] + intDeltaX, self.tuImagePos[1] + intDeltaY)

    def moveImage(self, x, y):
        """
        X: Desired X location
        Y: Desired Y location
        Automatically clamps to the edges of the image.
        """

        self.x = self.inRange(x, 0, self.pUsedImage.width - self.width)
        self.y = self.inRange(y, 0, self.pUsedImage.height - self.height)

        self.tuNewPos = (self.x, self.y)

        pNewImage = self.pUsedImage.transform(self.pUsedImage.size, Image.AFFINE, (1, 0, self.tuNewPos[0], 0, 1, self.tuNewPos[1]))
        self.pImage = self.compileImage(pNewImage)

        super().config(image = self.pImage)

    def scaleImage(self, flZoomAmount = 0.1):
        """
        flZoomAmount: How much to scale the Image by. Negative numbers to scale out.

        Clamps at X10, and smallest allowed unzoom.
        """

        if self.bNoImage:
            return

        flNewScale = self.flImageScale + flZoomAmount

        if flNewScale > 2:
            print("Image is absurdly big! Clamping!")
            return

        intImageWidth = floor(self.intOriginalWidth * flNewScale)
        intImageHeight = floor(self.intOriginalHeight * flNewScale)

        if intImageWidth < self.width or intImageHeight < self.height:
            print("Image is going to be too small! Clamping!")
            return

        pNewImage = self.pRawImage.resize((intImageWidth, intImageHeight))
        self.pUsedImage = pNewImage

        intDiffWidth = self.intOriginalWidth * flZoomAmount
        intDiffHeight = self.intOriginalHeight * flZoomAmount

        print(f"{intDiffWidth}, {intDiffHeight}")

        intNewX = floor(self.tuImagePos[0] + (intDiffWidth / 2))
        intNewY = floor(self.tuImagePos[1] + (intDiffHeight / 2))

        print(f"Size: Width: {self.pUsedImage.width}, Height: {self.pUsedImage.height}")
        print(f"New Pos: X:{intNewX}, Y:{intNewY}")

        self.moveImage(intNewX, intNewY)

        self.tuImagePos = (intNewX, intNewY)

        self.flImageScale = flNewScale

        print(f"Scaling at: x{self.flImageScale}")

        return

    def mouseScroll(self, rEvent):
        """
        Called when the scrollwheel is moved on the mouse
        Used to zoom in or out of the picture.
        """
        print(rEvent)

        if(rEvent.num == 4 or rEvent.delta > 0):
            self.scaleImage(0.1)
        else:
            self.scaleImage(-0.1)


    def mouseRelease(self, rEvent):
        """
        Called when the LMB is release, this is used to
        reset the start position of the mouse when LMB is pressed.
        """
        print("Mouse Released!")
        self.tuImagePos = self.tuNewPos
        self.tuStartPos = None
        print(self.tuImagePos)
        return

    def inRange(self, intNum, intMin, intMax):
        intNum = self.max(intNum, intMin)
        intNum = self.min(intNum, intMax)
        return intNum

    def max(self, intOne, intTwo):
        if(intOne > intTwo):
            return intOne
        return intTwo

    def min(self, intOne, intTwo):
        if(intOne < intTwo):
            return intOne
        return intTwo
