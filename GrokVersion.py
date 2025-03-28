import tkinter as tk
from tkinter import font as tkFont
import random

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("950x900+0+0")
        self.theCanvas = tk.Canvas(self, width=800, height=900, bg="#ddddff")
        self.theCanvas.grid(row=0, column=0, rowspan=4)
        self.buttonfont = tkFont.Font(family="Consolas", weight="bold")

        self.button1 = tk.Button(self, text="Done", font=self.buttonfont, command=self.doneclicked)
        self.button1.grid(row=1, column=1, sticky="NSEW")
        self.button2 = tk.Button(self, text="Undo", font=self.buttonfont, command=self.undoclicked)
        self.button2.grid(row=2, column=1, sticky="NSEW")
        self.rowconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.theCanvas.bind("<Motion>", self.mouseMoved)
        self.theCanvas.bind("<Button-1>", self.mouseClicked)

        self.movetext = None
        self.infotext = None
        self.stonepic = tk.PhotoImage(file="stone.png")
        self.statustext = self.theCanvas.create_text(400, 50, text="Your turn", font=("Consolas", 20), anchor="center")

        self.columnchosen = None
        self.numberchosen = 0
        self.gamestate = 0  # 0: player's turn, 1: computer's turn, 2: game over
        self.stonepics = []
        self.setupGame()

    def doneclicked(self):
        if self.gamestate != 0:
            return
        print("Player move done")
        self.piles[self.columnchosen] -= self.numberchosen
        self.columnchosen = None
        self.numberchosen = 0
        self.drawBoard()
        if sum(self.piles) == 0:
            self.theCanvas.itemconfig(self.statustext, text="You win!")
            self.gamestate = 2
        else:
            self.gamestate = 1
            self.theCanvas.itemconfig(self.statustext, text="Computer's turn")
            self.after(1000, self.computerMove)

    def undoclicked(self):
        if self.gamestate != 0:
            return
        self.columnchosen = None
        self.numberchosen = 0
        self.drawBoard()

    def mouseMoved(self, e):
        self.theCanvas.delete(self.movetext)
        self.movetext = self.theCanvas.create_text(20, 20, text=f"moved to {e.x}, {e.y}", anchor="nw")

    def mouseClicked(self, e):
        if self.gamestate != 0:
            return
        column = e.x // 200
        self.theCanvas.delete(self.infotext)
        self.infotext = self.theCanvas.create_text(750, 20, text=f"Chose Column {column}", anchor="ne")
        if self.columnchosen is None:
            self.columnchosen = column
        if self.columnchosen != column:
            self.theCanvas.itemconfig(self.infotext, text="You can only choose one pile")
        else:
            self.theCanvas.itemconfig(self.infotext, text="OK")
            self.numberchosen += 1
            if self.piles[self.columnchosen] < self.numberchosen:
                self.numberchosen = self.piles[self.columnchosen]
            self.drawBoard()

    def setupGame(self):
        self.piles = [7, 5, 3, 1]
        self.drawBoard()

    def drawBoard(self):
        # Delete all the old stone pictures
        for s in self.stonepics:
            self.theCanvas.delete(s)
        self.stonepics = []
        # Draw the piles of stones
        y = 300
        x = 100
        for pilenum in range(len(self.piles)):
            if pilenum == self.columnchosen:
                reduction = self.numberchosen
            else:
                reduction = 0
            for stoneNum in range(self.piles[pilenum] - reduction):
                self.stonepics.append(self.theCanvas.create_image(x, y, image=self.stonepic))
                y += 50
            x += 200
            y = 300

    def computerMove(self):
        available_piles = [i for i in range(len(self.piles)) if self.piles[i] > 0]
        if available_piles:
            pilechosen = random.choice(available_piles)
            numberchosen = random.randint(1, self.piles[pilechosen])
            self.piles[pilechosen] -= numberchosen
            self.theCanvas.itemconfig(self.infotext, text=f"Computer removed {numberchosen} from pile {pilechosen + 1}")
            self.drawBoard()
            if sum(self.piles) == 0:
                self.theCanvas.itemconfig(self.statustext, text="Computer wins!")
                self.gamestate = 2
            else:
                self.gamestate = 0
                self.theCanvas.itemconfig(self.statustext, text="Your turn")

app = Main()
app.mainloop()