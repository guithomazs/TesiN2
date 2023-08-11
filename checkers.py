from tkinter import *

EVEN_TILES = 'white'  # blocos pares
ODD_TILES = 'brown'   # blocos ímpares
PLAYER_ONE_COLOR = 'red'
PLAYER_TWO_COLOR = 'black'

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
        self.player_one_remaining = 12
        self.player_two_remaining = 12
        self.player_turn = True
        self.clicked = False
        self.createHeader()
        self.createStartBoard()

    def createHeader(self):
        self.frameHeader = Frame(self.root)
        titleFont = 'Helvetica 16 bold'
        subFont = 'Helvetica 12'

        framePlayerOne = Frame(self.frameHeader)
        Label(framePlayerOne, 
                 text='Jogador 1', 
                 font=titleFont, 
                #  fg=PLAYER_ONE_COLOR
        ).grid()
        self.LabelPlayerOneCards = Label(
            framePlayerOne, 
            text=f'Peças Restantes: {self.player_one_remaining}', 
            font=subFont,
            # fg=PLAYER_ONE_COLOR
        )
        self.LabelPlayerOneCards.grid()
        
        frameTurn = Frame(self.frameHeader)
        Label(frameTurn, 
                 text='Vez do jogador:', 
                 font=titleFont
        ).grid()
        self.LabelTurn = Label(
            frameTurn, 
            text=1 if self.player_turn else 2, 
            font=subFont
        )
        self.LabelTurn.grid()

        framePlayerTwo = Frame(self.frameHeader)
        Label(
            framePlayerTwo, 
            text='Jogador 2', 
            font=titleFont, 
            # fg=PLAYER_TWO_COLOR
        ).grid()
        self.LabelPlayerTwoCards = Label(
            framePlayerTwo, 
            text=f'Peças restantes: {self.player_two_remaining}', 
            font=subFont,
            # fg=PLAYER_TWO_COLOR
        )
        self.LabelPlayerTwoCards.grid()

        framePlayerOne.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=NSEW)
        frameTurn.grid(row=0, column=2, rowspan=2, sticky=NSEW)
        framePlayerTwo.grid(row=0, column=4, rowspan=2, sticky=NSEW)
        self.frameHeader.grid_columnconfigure(1, weight=1)
        self.frameHeader.grid_columnconfigure(3, weight=1)
    
        self.frameHeader.grid(sticky=NSEW)

    def createStartBoard(self):
        self.game_table = [[None for j in range(8)] for i in range(8)]
        for row in range(3):
            for column in range(8):
                self.game_table[row][column] = (
                    False if (is_odd(row) and not is_odd(column))
                        or not is_odd(row) and is_odd(column)
                    else None
                )
        for row in range(5, 8):
            for column in range(8):
                self.game_table[row][column] = (
                    True if (is_odd(row) and not is_odd(column)) 
                        or not is_odd(row) and is_odd(column)
                    else None
                )
        self.createTable()

    def createTable(self):
        self.slots_frame = Frame(self.root)
        for i in range(8):
            for j in range(8):
                self.createElement(i, j)
        self.slots_frame.grid()

    def createElement(self, row, column):
        lbl = Label(self.slots_frame,
                        bg=self.get_tile_color(row, column),
                        fg=self.get_tile_foreground(row, column),
                        text=self.get_tile_text(row, column),
                        width=4, height=2,
                        font='None 18 bold'
                        )
        lbl.bind('<<ButtonPress-1>>', lambda lbl=lbl, row=row, column=column: self.checkMovement(lbl, row, column))
        lbl.bind('<<ButtonPress-3>>', lambda lbl=lbl, row=row, column=column: self.checkMovement(lbl, row, column))
        lbl.grid(row=row, column=column)

    def checkMovement(lbl, row, column):
        print(lbl)
        

    def get_tile_color(self, row, column):
        return (EVEN_TILES if (is_odd(row) and not is_odd(column)) 
                    or not is_odd(row) and is_odd(column) else ODD_TILES )

    def get_tile_foreground(self, row, column):
        return (PLAYER_ONE_COLOR if self.game_table[row][column] == True 
                else PLAYER_TWO_COLOR if self.game_table[row][column] == False 
                else None)
    
    def get_tile_text(self, row, column):
        return ('⛃' if self.game_table[row][column] is not None else '')
root = Tk()
app = Checkers(root)
root.mainloop()