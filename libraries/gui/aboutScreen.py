"""
Created on Jul 16, 2021

Author: BP
"""

import tkinter as tk
from math import floor

class AboutScreen(tk.Toplevel):
    """
    A top level widget which provides information on this tool.
    """

    def __init__(self, master):
        super().__init__(master)

        self.master = master

        flAspectRatio = 3/2
        nWidth = floor(self.winfo_screenwidth() / 5)
        nHeight = floor(nWidth / flAspectRatio)

        self.title("About")
        self.resizable(False, False)
        self.geometry(f"{nWidth}x{nHeight}")

        self.renderScene()

        self.mainloop()

    def renderScene(self):
        pFrame = tk.Frame(self)
        pFrame.pack(expand=True, fill=tk.BOTH)
        pTitle = tk.Label(pFrame, text="Custom Map Compiler", font=("Arial", 20))
        pTitle.place(relx=0.5, rely=0.1, anchor="center")
