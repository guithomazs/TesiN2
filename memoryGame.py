import tkinter as tk
import random

def showMat(mat):
    for i in range(5):
        for j in range(6):
            print(mat[i][j], ' ', end='')
        print()

class MemoryGame:
    def __init__(self, master:tk.Tk()) -> None:
        self.root = master
        self.root.resizable(False, False) 
        self.root.title('Memory Game in tkinter')
        self.emojiList = [
            '😀', '😄', '😁', '😆', '😅', 
            '😂', '🤣', '🤑', '🤠', '😈', 
            '👹', '👺', '🤡', '💩', '👻', 
        ]
        self.startGame()

    def startGame(self):
        '''
        we are playing with 15 emojis as the items, 
        so the window game will have 5 rows and 6 
        columns what means it will have 30 slots.
        '''
        self.slots = [[None for column in range(6)] for row in range(5)]
        self.fillSlots()

    def fillSlots(self):
        freeSlots = [[row, column] for column in range(6) for row in range(5)]
        for item in self.emojiList:
            slot1, slot2 = random.sample(freeSlots, k=2)
            freeSlots.pop(freeSlots.index(slot1))
            freeSlots.pop(freeSlots.index(slot2))
            self.slots[slot1[0]][slot1[1]] = item
            self.slots[slot2[0]][slot2[1]] = item

        showMat(self.slots)


if __name__ == '__main__':
    root = tk.Tk()
    # app = MemoryGame(root)
    root.mainloop()