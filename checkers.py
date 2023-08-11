from tkinter import *

EVEN_TILES = 'black'  # blocos pares
ODD_TILES = 'white'   # blocos ímpares

def showMat(mat):
    for i in range(8):
        for j in range(8):
            print(mat[i][j], ' ', end='')
        print()

def is_odd(number):
    return True if number % 2 != 0 else False

class Checkers:
    def __init__(self, master=Tk) -> None:
        self.root = master
        self.root.resizable(False, False)
        self.root.title('Checkers in tkinter')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.startGame()

    def startGame(self):
        start_table = [[0 for j in range(8)] for i in range(8)]
        for row in range(3):
            for column in range(8):
                start_table[row][column] = (
                    False if (is_odd(row) and not is_odd(column))
                        or not is_odd(row) and is_odd(column)
                    else None
                )

        for row in range(5, 8):
            for column in range(8):
                start_table[row][column] = (
                    True if (is_odd(row) and not is_odd(column)) 
                        or not is_odd(row) and is_odd(column)
                    else None
                )

        showMat(start_table)

root = Tk()
app = Checkers(root)
root.mainloop()