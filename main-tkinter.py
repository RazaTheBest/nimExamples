import tkinter as tk
from tkinter import font as tkFont
import random

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("950x900+0+0")
        self.theCanvas = tk.Canvas(self,width=800, height=900, bg="#ddddff")
        self.theCanvas.grid(row=0, column=0)
        self.buttonfont = tkFont.Font(family="Consolas", weight="bold")

        self.button1 = tk.Button(self, text="Normal Button", font=self.buttonfont, command = self.buttonClicked)
        self.button1.grid(row=0, column=1)

        self.theCanvas.bind("<Motion>", self.mouseMoved)
        self.theCanvas.bind("<Button-1>", self.mouseClicked)

        self.buttonPic = tk.PhotoImage(file="button.png")
        self.stonePic = tk.PhotoImage(file="Stone.png")
        self.clicked = tk.PhotoImage(file="click.png")
        
        self.canvasbutton = self.theCanvas.create_image(200,800,image = self.buttonPic)
        self.theCanvas.tag_bind(self.canvasbutton, "<Button-1>", self.canvasButtonClicked)
        
        self.movetext = None
        self.clickText = None
        self.buttonText = None
        self.piles= [7,5,3,1]
        self.drawPiles()
        self.mainloop()

    def drawPiles(self):
        for p in range(7):
            y=100
            for i in pilesize:
                self.theCanvas.create_image(x,y,image = self.stonePic)
                y = y +50
            x = x + 60


    def buttonClicked(self):
        x = random.randint(100,700)
        y = random.randint(100,700)
        self.theCanvas.delete(self.buttonText)
        self.buttonText = self.theCanvas.create_text(x,y,text="tkinter Button clicked")
 
    def mouseMoved(self,e):
        self.theCanvas.delete(self.movetext)
        self.movetext = self.theCanvas.create_text(20,20, text=f"moved to {e.x}, {e.y}", anchor="nw")

    def mouseClicked(self,e):
        self.theCanvas.delete(self.clickText)
        self.clickText = self.theCanvas.create_text(750,20, text=f"Clicked at {e.x}, {e.y}", anchor="ne")

    def canvasButtonClicked(self,e):
        self.theCanvas.itemconfigure(self.canvasbutton,image=self.clicked )
        self.after(1000,self.restorebutton)

    def restorebutton(self):
        self.theCanvas.itemconfigure(self.canvasbutton,image=self.buttonPic )


app = Main()


        
