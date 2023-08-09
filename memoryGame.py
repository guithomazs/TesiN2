import tkinter as tk
import time
import random

GAME_ROWS = 5
GAME_COLUMNS = 6
def showMat(mat):
    for i in range(GAME_ROWS):
        for j in range(GAME_COLUMNS):
            print(mat[i][j], ' ', end='')
        print()

class MemoryGame:
    def __init__(self, master:tk.Tk):
        self.root = master
        self.root.resizable(False, False) 
        self.root.title('Memory Game in tkinter')
        self.emojiList = [
            '😀', '😄', '😁', '😆', '😅', 
            '😂', '🤣', '🤑', '🤠', '😈', 
            '👹', '👺', '🤡', '💩', '👻', 
        ]
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.startGame()

    def startGame(self):
        '''
        we are playing with 15 emojis as the items, 
        so the window game will have 5 rows and 6 
        columns what means it will have 30 slots.
        '''
        self.slots = [[None for column in range(GAME_COLUMNS)] for row in range(GAME_ROWS)]
        self.choiceOne, self.choiceTwo, self.ButtonOne, self.ButtonTwo = None, None, None, None
        self.discovered = 0
        self.fillSlots()
        self.createButtons()

    def fillSlots(self):
        freeSlots = [[row, column] for column in range(GAME_COLUMNS) for row in range(GAME_ROWS)]
        for item in self.emojiList:
            slot1, slot2 = random.sample(freeSlots, k=2)
            freeSlots.pop(freeSlots.index(slot1))
            freeSlots.pop(freeSlots.index(slot2))
            self.slots[slot1[0]][slot1[1]] = item
            self.slots[slot2[0]][slot2[1]] = item

        showMat(self.slots)
    
    def createButtons(self):
        self.frameButtons = tk.Frame(self.root)
        self.buttonsList = []
        for row in range(GAME_ROWS):
            for column in range(GAME_COLUMNS):
                btn = tk.Button(self.frameButtons, text='', \
                        width=5, height=2, relief='solid', font='None 28 bold', \
                        # command=lambda position=(row, column):self.control(position))
                )
                self.buttonsList.append(btn)
                btn.bind("<ButtonPress-1>", 
                         lambda 
                         event, 
                         button=self.buttonsList[-1],
                         position=(row, column)
                         :
                         self.control(button, position))
                btn.grid(row=row, column=column, sticky=tk.NSEW, padx=1, pady=1)
        self.frameButtons.grid()

    def control(self, button, position):
        if not self.choiceOne:
            self.ButtonOne = button
            self.click1(button, position)
        elif not self.choiceTwo:
            self.ButtonTwo = button
            self.click2(button, position)

    def click1(self, button:tk.Button, position):
        row, column = position
        self.choiceOne = self.slots[row][column]
        button.config(text=self.choiceOne)

    def click2(self, button:tk.Button, position):
        row, column = position
        self.choiceTwo = self.slots[row][column]
        print(self.choiceOne, self.choiceTwo)
        button.config(text=self.choiceTwo)
        self.validate()

    def validate(self):
        if self.choiceOne == self.choiceTwo:
            self.discovered += 1
            self.choiceOne, self.choiceTwo = None, None
            self.ButtonOne.unbind("<ButtonPress-1>")
            self.ButtonTwo.unbind("<ButtonPress-1>")
            self.ButtonOne, self.ButtonTwo = None, None
        else:
            self.ButtonOne.config(text='')
            self.ButtonTwo.config(text='')
            self.choiceOne, self.choiceTwo = None, None


root = tk.Tk()
app = MemoryGame(root)
root.mainloop()
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = MemoryGame(root)
#     root.mainloop()