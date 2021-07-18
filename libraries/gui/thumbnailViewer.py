"""
Author: Builderpro
File: C:/Users/Builderpro/eclipse-workspace/BonusMapCompiler/libraries/gui/thumbnailViewer.py
Reason: Allows the user to drag and drop an image, then allow the user to drag around the image and zoom with the scroll wheel.
        The displayed thumbnail can be outputted.
"""

import tkinter as tk
from PIL import Image, ImageTk
from math import floor, ceil

class ThumbnailViewer(tk.Canvas):

    def __init__(self, master, strDefaultImage = "./assets/mapDefault.png", *args, **kwargs):

        #kwargs["anchor"] = kwargs.get("anchor", "nw")
        #kwargs["padx"] = kwargs.get("padx", 0)
        #kwargs["pady"] = kwargs.get("pady", 0)
        #kwargs["bd"] = kwargs.get("bd", 0)

        super().__init__(master, *args, **kwargs)

        self.master = master

        self.width = None
        self.height = None

        #The PIL and ImageTK intance.
        self.pRawImage = None
        self.pImage = None
        #The index for which the canvas image is at.
        self.nCanvasImage = None

        self.initGeometry(kwargs)

        self.setImage(strDefaultImage)
        self.bNoImage = True #Prevents the user from scaling mapDefault.tga

        #Event Related Stuff
        self.bMouseOver = False

        self.tuOriginalSize = None #Width/Height of the image at x1.0
        self.tuScaledSize = None #Size of the scaled image.
        self.tuImagePos = None #Position of the image.
        self.nRightStop = None #How far can the user pan rightwards.
        self.nBottomStop = None #How far the user can pan downwards.
        self.tuMousePos = None #Record the position of the mouse when it's first pressed down, in order to move the image relative to the pos.
        self.flImageScale = 1 #The scale of the image, floats round up on resolution.

        #self.intOriginalWidth = self.pRawImage.width
        #self.intOriginalHeight = self.pRawImage.height
        #Moving Image
        self.bind("<Button-1>", self.initMouseMove)
        self.bind("<B1-Motion>", self.mouseMoveImage)
        self.bind("<ButtonRelease-1>", self.mouseRelease)

        #Scaling
        self.bind("<MouseWheel>", self.mouseScroll)
        #Linux mouse wheel
        self.bind("<Button-4>", self.mouseScroll)
        self.bind("<Button-5>", self.mouseScroll)

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

        pScaledImage = self.pRawImage.resize(self.tuScaledSize)

        x = self.tuImagePos[0] * -1
        y = self.tuImagePos[1] * -1
        #We will calculate the aspect ratio again.
        nWidth = self.winfo_width()
        nHeight = self.winfo_height()

        #A long ass line which resizes the raw image to the current scale, then crop it to the current selection.
        return pScaledImage.crop((x, y, x + nWidth, y + nHeight))

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
        #Check to see if we already have an image.
        if self.pRawImage:
            #We do. Assume that it's on the canvas as well.
            self.pRawImage.close()
            self.delete(self.nCanvasImage)
            self.nCanvasImage = None

        #Open the Image and convert it to a TK compatable image.
        self.pRawImage = Image.open(strImagePath)

        #Get the ratio of the image's side respective to the widget.
        flWidthRatio = self.pRawImage.width / self.width
        flHeightRatio = self.pRawImage.height / self.height
        #Check to see which side is lesser, then set that lesser side to the respective size of the side of the widget.
        tuNewSize = None
        if flWidthRatio < flHeightRatio:
            #Width is lesser.
            nWidth = self.width
            nHeight = floor((self.pRawImage.height * nWidth)/self.pRawImage.width)
            tuNewSize = (nWidth, nHeight)
        else:
            #Height is lesser.
            nHeight = self.height
            nWidth = floor((self.pRawImage.width * nHeight)/self.pRawImage.height)
            tuNewSize = (nWidth, nHeight)

        #Rescale the image and set it as the canvas element.
        pScaledImage = self.pRawImage.resize(tuNewSize, Image.LANCZOS)
        self.flImageScale = 1
        self.tuScaledSize = tuNewSize
        self.tuOriginalSize = tuNewSize #All scales will be based off of this one.
        self.nRightStop = self.width - tuNewSize[0]
        self.nBottomStop = self.height - tuNewSize[1]
        self.pImage = ImageTk.PhotoImage(pScaledImage)
        #We also move the image to the middle of the screen.
        nMiddleWidth = floor((self.tuScaledSize[0] - self.width) / -2)
        nMiddleHeight = floor((self.tuScaledSize[1] - self.height) / -2) #We must make this one a negative as the height is inverted.
        self.tuImagePos = (nMiddleWidth, nMiddleHeight)
        self.nCanvasImage = self.create_image(nMiddleWidth, nMiddleHeight, image=self.pImage, anchor="nw")
        pScaledImage.close()

        self.bNoImage = False

        self.master.event_generate("<<ThumbnailNewImage>>")

        return

    def initMouseMove(self, rEvent):
        """
        Called when the user clicks down.
        Sets up the position.
        """
        pass

    def mouseMoveImage(self, rEvent):
        """
        Called when the mouse clicks and drags over the widget.
        Moves the image inside of the frame.
        """

        if self.bNoImage:
            return

        if not self.tuMousePos:
            self.tuMousePos = (rEvent.x, rEvent.y)

        intDeltaX = self.tuMousePos[0] - rEvent.x
        intDeltaY = self.tuMousePos[1] - rEvent.y

        self.moveImage(self. tuImagePos[0] - intDeltaX, self.tuImagePos[1] - intDeltaY)

    def moveImage(self, x, y):
        """
        X: Desired floorX location
        Y: Desired Y location
        Automatically clamps to the edges of the image.
        """
        x = self.inRange(x, self.nRightStop, 0)
        y = self.inRange(y, self.nBottomStop, 0)

        tuNewPos = (x, y)

        #self.tuImagePos = tuNewPos

        self.coords(self.nCanvasImage, tuNewPos)

    def setPos(self, x, y):
        """
        Move image and set the new position.
        """
        self.moveImage(x, y)
        self.tuNewPos = (x, y)

    def scaleImage(self, flZoomAmount = 0.1):
        """
        flZoomAmount: How much to scale the Image by. Negative numbers to scale out.

        Clamps at X2, and smallest allowed unzoom.
        """
        #Do nothing if there is no image.nCanvasImage
        if self.bNoImage:
            return

        #Get the new scale.
        flNewScale = self.flImageScale + flZoomAmount

        #Check to make sure it's not above our clamp.
        if flNewScale > 2:
            #print("Image is absurdly big! Clamping!")
            return
        #Get the new size
        intImageWidth = floor(self.tuOriginalSize[0] * flNewScale)
        intImageHeight = floor(self.tuOriginalSize[1] * flNewScale)
        #Make sure that the new size will not expost the canvas' background.
        #IE. too small.
        if intImageWidth < self.winfo_width() or intImageHeight < self.winfo_height():
            #print("Image is going to be too small! Clamping!")
            return
        #Everything's all good, Set to new scale.
        self.flImageScale = flNewScale
        self.tuScaledSize = (intImageWidth, intImageHeight)
        self.nRightStop = self.width - self.tuScaledSize[0]
        self.nBottomStop = self.height - self.tuScaledSize[1]
        #Set the current image to a reszied one.
        pNewImage = self.pRawImage.resize(self.tuScaledSize)
        #Get the new coords based off of the position of image..
        nXOffset = floor(-abs((self.tuImagePos[0] * flNewScale)))
        nYOffset = floor(-abs((self.tuImagePos[1] * flNewScale)))
        #Now change the position to reflect where it currently is.
        #Also make sure it's in the bounds of the image.
        intNewX = min(0, max(nXOffset, self.nRightStop))
        intNewY = min(0, max(nYOffset, self.nBottomStop))

        #Now place the new image on the canvas.
        self.delete(self.nCanvasImage)
        self.pImage = ImageTk.PhotoImage(pNewImage)
        self.nCanvasImage = self.create_image(intNewX, intNewY, image=self.pImage, anchor="nw")
        self.tuImagePos = (intNewX, intNewY)

        return

    def setScale(self, flZoom: float):
        self.scaleImage(flZoom - self.flImageScale)

    def mouseScroll(self, rEvent):
        """
        Called when the scrollwheel is moved on the mouse
        Used to zoom in or out of the picture.
        """

        if(rEvent.num == 4 or rEvent.delta > 0):
            self.scaleImage(0.1)
        else:
            self.scaleImage(-0.1)


    def mouseRelease(self, rEvent):
        """
        Called when the LMB is release, this is used to
        reset the start position of the mouse when LMB is pressed.
        """
        self.tuImagePos = self.coords(self.nCanvasImage)
        self.tuMousePos = None
        return

    def inRange(self, intNum, intMin, intMax):
        return min(max(intNum, intMin), intMax)

    def updateSize(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        #print(9/5)
        #print(self.width/self.height)

    def getPos(self):
        return self.tuImagePos

    def getScale(self):
        return self.flImageScale

    #Packing overriding to allow for changing the width and height
    def grid(self, *args, **kvars):
        super().grid(*args, **kvars)
        self.after(1,self.updateSize)

    def pack(self, *args, **kvars):
        super().pack(*args, **kvars)
        self.after(1,self.updateSize)

    def place(self, *args, **kvars):
        super().place(*args, **kvars)
        self.after(1,self.updateSize)
