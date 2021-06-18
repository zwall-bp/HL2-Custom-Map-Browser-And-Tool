"""

    SplashScreen

    The first window that pops up. Allows the user to select either creating a single map, or a map pack.

"""

import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
from math import floor
import os
import random

class SplashScreen(tk.Tk):

    """
        Before booting up the main program, ask the user if they
        will be making a single map or map pack.
    """

    def __init__(self):
        super().__init__()
        self.title("Bonus Map Splash")
        self.geometry("600x250")
        self.resizable(False, False)
        self.strReturnVal = None

        self.pFilter = ImageFilter.GaussianBlur(2) #The filter that should be used in the foregound.
        self.rImages = []

        self.getBackgroundImages()
        self.selectBackgroundImage()

        self.renderScene()

        self.bind("<Motion>", self.MouseMovement)
        self.bind("<space>", self.selectBackgroundImage)

        self.mainloop()

    def GetSelection(self):
        return self.strReturnVal

    def renderScene(self):
        self.pImage = self.strSelectedImage
        self.pBackground = self.compileImg(self.pImage)
        self.pPixel = tk.PhotoImage(width = 1, height = 1)
        self.pForeground = self.blurImg(self.pImage, self.pFilter)

        self.pBackgroundIm = tk.Label(self, image = self.pBackground, bd = 0, padx = 0, pady = 0)
        self.pBackgroundIm.place(relx = 0.5, rely = 0.5, anchor = "center")

        #pCanvas = tk.Frame(self, bg="red")
        #pCanvas.pack(fill = "both", expand = True)

        self.pTitle = tk.Label(self, text = "Custom Map Compiler", font = ("MS PMincho Regular", 35), anchor = "center", compound = "center", relief = "raised", pady = 0, padx = 0, bd = 0, fg = "gainsboro")

        self.pTitle.place(relx = 0.5, rely= 0.2, anchor ="center")

        self.pSingleButton = tk.Button(self,
            text= "Single Map",
            anchor= "center",
            font = ("MS PMincho Regular", 20),
            width = 150,
            height = 80,
            padx = 0,
            pady = 0,
            bd = 0,
            compound = "center",
            image = self.pPixel,
            fg = "gainsboro",
            command = self.StartSingle
        )

        self.pPackButton = tk.Button(self,
            text= "Map Pack",
            anchor = "center",
            font = ("MS PMincho Regular", 20),
            width = 150,
            height = 80,
            padx = 0,
            pady = 0,
            bd = 0,
            compound = "center",
            image = self.pPixel,
            fg = "gainsboro",
            command = self.StartPack
        )

        #pSingleButton.grid(row = 1)
        #pPackButton.grid(row = 1, column = 1)

        self.pSingleButton.place(relx = 0.3, rely = 0.7, anchor= "center")
        self.pPackButton.place(relx = 0.7, rely = 0.7, anchor= "center")

        self.update()

        pTempForeground = self.pForeground.transform(self.pForeground.size, Image.AFFINE, (1, 0, self.pBackgroundIm.winfo_x() * -1, 0, 1, self.pBackgroundIm.winfo_y() * -1))

        self.pWidgetImage = self.compileImg(self.cropWidget(self.pTitle, pTempForeground))
        self.pSingleImage = self.compileImg(self.cropWidget(self.pSingleButton, pTempForeground))
        self.pPackImage = self.compileImg(self.cropWidget(self.pPackButton, pTempForeground))

        pTempForeground.close()

        self.pTitle.configure(image = self.pWidgetImage)
        self.pSingleButton.configure(image = self.pSingleImage)
        self.pPackButton.configure(image = self.pPackImage)

    #User wants to make a single bonus map
    def StartSingle(self):
        self.strReturnVal = "single"
        self.destroy()
        return

    #User wants to make a bonus map pack
    def StartPack(self):
        self.strReturnVal = "pack"
        self.destroy()
        return

    def MouseMovement(self, *args):
        x, y = self.winfo_pointerx() - self.winfo_rootx(), self.winfo_pointery() - self.winfo_rooty()

        #print(f"X:{x} Y:{y}")

        x -= self.winfo_width() / 2
        y -= self.winfo_height() / 2

        intXPos, intYPos = (x * -1), (y * -1)

        self.pBackgroundIm.place(x = intXPos, y = intYPos)

        pTempForeground = self.pForeground.transform(self.pForeground.size, Image.AFFINE, (1, 0, self.pBackgroundIm.winfo_x() * -1, 0, 1, self.pBackgroundIm.winfo_y() * -1))

        self.pWidgetImage = self.compileImg(self.cropWidget(self.pTitle, pTempForeground))
        self.pSingleImage = self.compileImg(self.cropWidget(self.pSingleButton, pTempForeground))
        self.pPackImage = self.compileImg(self.cropWidget(self.pPackButton, pTempForeground))

        """
        self.pTitle.get("image").close()
        self.pSingleButton.get("image").close()
        self.pPackButton.get("image").close()
        """
        pTempForeground.close()

        self.pTitle.configure(image = self.pWidgetImage)
        self.pSingleButton.configure(image = self.pSingleImage)
        self.pPackButton.configure(image = self.pPackImage)

        return

    def printWidgetInfo(self, pWidget):
        print(pWidget.winfo_x())
        print(pWidget.winfo_reqwidth())
        print(pWidget.winfo_y())
        print(pWidget.winfo_reqheight())
        print("")

    def blurLoadImg(self, strImg, pFilterType = ImageFilter.GaussianBlur()):
        """
            Input in the directory of an image, and filter it.
        """
        pImg = Image.open(strImg)
        return pImg.filter(pFilterType)

    def blurImg(self, pImg, pFilterType = ImageFilter.GaussianBlur()):
        return pImg.filter(pFilterType)

    def compileImg(self, pImg):
        pCompiledImg = ImageTk.PhotoImage(pImg)
        return pCompiledImg

    def widgetOverlay(self, pWidget, pImage, pFilterType = ImageFilter.GaussianBlur()):
        """
            Compiles all cropWidget(), blurImg(), and compileImg() into
            A single method!
        """

        pCroppedImage = self.cropWidget(pWidget, pImage)
        pBlurredImage = self.blurImg(pCroppedImage, pFilterType)

        return self.compileImg(pBlurredImage)

    def cropWidget(self, pWidget, pImage):
        """
        Returns an Image of the blurred cropped part of pImage.
        pWidget should first already be packed, use this, apply it, than update()
        pImage should NOT be compiled! (Dont use ImageTk.PhotoImage pointers)
        """
        intLeftStart = pWidget.winfo_x()
        intWidth = pWidget.winfo_reqwidth()
        intTopStart = pWidget.winfo_y()
        intHeight = pWidget.winfo_reqheight()

        #pImage = pImage.transform(pImage.size, Image.AFFINE, (1, 0, self.pBackgroundIm.winfo_x() * -1, 0, 1, self.pBackgroundIm.winfo_y() * -1))

        rBounds = (intLeftStart, intTopStart, intLeftStart + intWidth, intTopStart + intHeight)

        pImage = pImage.crop(rBounds)

        return pImage

    def getBackgroundImages(self):
        self.rImages = []

        intWindowWidth = 600 * 2.5 #Width is hard coded!

        for file in os.listdir("assets/backgrounds"):
            if file.endswith(".jpg") or file.endswith(".png"):
                strFileLocation = f"./assets/backgrounds/{file}"
                pImage = Image.open(strFileLocation)

                if pImage.width != intWindowWidth: #Checks to see if the image has already been altered. If it's new, resize.
                    flSizeDiff = intWindowWidth / pImage.width
                    tuNewSize = (floor(pImage.width * flSizeDiff), floor(pImage.height * flSizeDiff))
                    pImage = pImage.resize(tuNewSize)

                    #Overwrite, and save a thumbnail of the new image, for faster loading in the future.
                    pImage.save(strFileLocation)
                    print(f"Found a new image, {strFileLocation}, converted and saved!")

                self.rImages.append(pImage)
        if not self.rImages:
            self.rImages.append(Image.new("RGB", (1, 1), color = (125, 125, 125)))
        self.shuffleImages()
        self.itrImages = iter(self.rImages)
        return

    def selectBackgroundImage(self, *args):
        pNextImage = next(self.itrImages, False)

        if(not pNextImage):
            print("Shuffling!")
            self.shuffleImages()
            print(self.rImages)
            self.itrImages = iter(self.rImages)
            pNextImage = next(self.itrImages, False)

        self.strSelectedImage = pNextImage

        if args:
            self.updateImages()

        return

    def updateImages(self):
        self.pImage = self.strSelectedImage

        self.pBackground = self.compileImg(self.pImage)
        self.pForeground = self.blurImg(self.pImage, self.pFilter)

        self.pBackgroundIm.configure(image = self.pBackground)
        pTempForeground = self.pForeground.transform(self.pForeground.size, Image.AFFINE, (1, 0, self.pBackgroundIm.winfo_x() * -1, 0, 1, self.pBackgroundIm.winfo_y() * -1))

        self.pWidgetImage = self.compileImg(self.cropWidget(self.pTitle, pTempForeground))
        self.pSingleImage = self.compileImg(self.cropWidget(self.pSingleButton, pTempForeground))
        self.pPackImage = self.compileImg(self.cropWidget(self.pPackButton, pTempForeground))

        self.pTitle.configure(image = self.pWidgetImage)
        self.pSingleButton.configure(image = self.pSingleImage)
        self.pPackButton.configure(image = self.pPackImage)

    def shuffleImages(self):
        random.shuffle(self.rImages)
        return

if __name__ == "__main__":
    print("Never use this to test! It needs to be ran by a script which has access to the assets/ directory!")
