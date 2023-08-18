from tkinter import *
from enum import Enum

EVEN_TILES = 'white'  # blocos pares
ODD_TILES = 'brown'   # blocos ímpares
PLAYER_ONE_COLOR = 'red'
PLAYER_TWO_COLOR = 'black'

class PlayerOne(Enum):
    DEFAULT_PIECE = 'PlayerOne'
    SUPER_PIECE = 'SuperPlayerOne'
    
class PlayerTwo(Enum):
    DEFAULT_PIECE = 'PlayerTwo'
    SUPER_PIECE = 'SuperPlayerTwo'

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
        self.player_turn = True  #  True pro jogador 1 e False pro jogador 2
        self.first_click = None
        self.player_one_pieces = []
        self.player_two_pieces = []
        self.obrigatory_movements = {}
        self.on_deletion = False
        self.can_change_first_click = True
        self.buttons = [[None for i in range(8)] for j in range(8)]
        self.createHeader()
        self.createStartBoard()

    def createHeader(self):
        self.frame_header = Frame(self.root)
        titleFont = 'Helvetica 16 bold'
        subFont = 'Helvetica 12'

        framePlayerOne = Frame(self.frame_header)
        Label(framePlayerOne, 
                 text='Jogador 1', 
                 font=titleFont, 
                #  fg=PLAYER_ONE_COLOR
        ).grid()
        self.label_player_one_cards = Label(
            framePlayerOne, 
            text=f'Peças Restantes: {self.player_one_remaining}', 
            font=subFont,
            # fg=PLAYER_ONE_COLOR
        )
        self.label_player_one_cards.grid()
        
        frameTurn = Frame(self.frame_header)
        Label(frameTurn, 
                 text='Vez do jogador:', 
                 font=titleFont
        ).grid()
        self.LabelTurn = Label(
            frameTurn, 
            text='1', 
            # text=1 if self.player_turn else 2, 
            font=subFont
        )
        self.LabelTurn.grid()

        framePlayerTwo = Frame(self.frame_header)
        Label(
            framePlayerTwo, 
            text='Jogador 2', 
            font=titleFont, 
            # fg=PLAYER_TWO_COLOR
        ).grid()
        self.label_player_two_cards = Label(
            framePlayerTwo, 
            text=f'Peças restantes: {self.player_two_remaining}', 
            font=subFont,
            # fg=PLAYER_TWO_COLOR
        )
        self.label_player_two_cards.grid()

        framePlayerOne.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=NSEW)
        frameTurn.grid(row=0, column=2, rowspan=2, sticky=NSEW)
        framePlayerTwo.grid(row=0, column=4, rowspan=2, sticky=NSEW)
        self.frame_header.grid_columnconfigure(1, weight=1)
        self.frame_header.grid_columnconfigure(3, weight=1)
    
        self.frame_header.grid(sticky=NSEW)

    def createStartBoard(self):
        self.game_table = [[None for j in range(8)] for i in range(8)]
        for row in range(3):
            for column in range(8):
                # quando em linhas impares, colocar as peças em colunas 
                # pares, e quando em linhas pares colocar as peças 
                # em colunas impares
                self.game_table[row][column] = (
                    PlayerTwo.DEFAULT_PIECE if (is_odd(row) and not is_odd(column))
                        or not is_odd(row) and is_odd(column)
                    else None
                )
                if (is_odd(row) and not is_odd(column)) or not is_odd(row) and is_odd(column):
                    self.player_two_pieces.append([row, column])

        for row in range(5, 8):
            for column in range(8):
                # quando em linhas impares, colocar as peças em colunas 
                # pares, e quando em linhas pares colocar as peças 
                # em colunas impares
                self.game_table[row][column] = (
                    PlayerOne.DEFAULT_PIECE if (is_odd(row) and not is_odd(column)) 
                        or not is_odd(row) and is_odd(column)
                    else None
                )
                if (is_odd(row) and not is_odd(column)) or not is_odd(row) and is_odd(column):
                    self.player_one_pieces.append([row, column])
        self.createTable()

    def createTable(self):
        self.frame_slots = Frame(self.root)
        for i in range(8):
            for j in range(8):
                self.createElement(i, j)
        self.frame_slots.grid()

    def createElement(self, row, column):
        lbl = Label(self.frame_slots,
                        bg=self.getTileColor(row, column),
                        fg=self.getTileForeground(row, column),
                        text=self.getTileText(row, column),
                        width=4, height=2,
                        font='None 22 bold',
                        )
        lbl.bind('<ButtonPress-1>', lambda event, lbl=lbl, row=row, column=column: self.checkMovement(lbl, row, column))
        lbl.grid(row=row, column=column)
        self.buttons[row][column] = lbl

    def checkMovement(self, clicked_label:Label, row, column):
        # this variable checks if the first movement of a piece or if it's a sequence of captures
        self.on_deletion = False
        
        # define the element to be moved
        if not self.first_click:
            # if there is any capture to be done, only be able to click the piece that can capture something
            if len(self.obrigatory_movements) and (row, column) not in self.obrigatory_movements.keys():
                return
            player_pieces = PlayerOne if self.player_turn else PlayerTwo
            if not (
                self.game_table[row][column] == player_pieces.DEFAULT_PIECE
                or
                self.game_table[row][column] == player_pieces.SUPER_PIECE
                ):
                return
            clicked_label.config(bg='lime')
            self.first_click = clicked_label
            return
        
        # if it isn't the first click, and is the same label of the first click, reset the click
        if self.first_click == clicked_label:
            if not self.can_change_first_click:
                return
            clicked_label.config(bg='white')
            self.first_click = None
            return
        
        # if the house it's trying to move it's occupied then it isn't able to move
        if self.game_table[row][column] is not None:
            return
        
        first_click_row = self.first_click.grid_info()['row']
        first_click_col = self.first_click.grid_info()['column']

        if (
            len(self.obrigatory_movements) and 
                [row, column] not in 
                    list(self.obrigatory_movements[(first_click_row, first_click_col)])
            ):
            return
        
        possible_moves = self.getAdjacentTiles(first_click_row, first_click_col)
        if not len(self.obrigatory_movements) and [row, column] not in possible_moves:
            return
        if len(self.obrigatory_movements):
            if[row, column] not in self.obrigatory_movements[(first_click_row, first_click_col)]:
                return
            self.removePiece(first_click_row, first_click_col, row, column)
            self.obrigatory_movements = {}
            self.changePiecePosition(first_click_row, first_click_col, row, column, clicked_label)    
            self.mapPiece(row, column)
        # self.checkNext(first_click_row, first_click_col, row, column)
        else:
            self.changePiecePosition(first_click_row, first_click_col, row, column, clicked_label)    

        if not len(self.obrigatory_movements):
            self.can_change_first_click = True
            self.changePlayerTurn()  
        else:
            self.can_change_first_click = False
            self.first_click = clicked_label
            clicked_label.config(bg='lime')

    def getAdjacentTiles(self, piece_row, piece_column):
        if self.game_table[piece_row][piece_column] in [PlayerOne.DEFAULT_PIECE, PlayerTwo.DEFAULT_PIECE]:
            # in default pieces, player 2 can only move 
            # downwards and player 1 can only move upwards 
            # if it's not for capture an enemy.
            return [
                    [piece_row-1, piece_column-1],
                    [piece_row-1, piece_column+1], 
                ] if self.player_turn else [
                    [piece_row+1, piece_column-1],
                    [piece_row+1, piece_column+1]
                    ]
        return [
            [piece_row-1, piece_column-1],
            [piece_row-1, piece_column+1], 
            [piece_row+1, piece_column-1],
            [piece_row+1, piece_column+1]
        ]

    def removePiece(self, first_row, first_column, last_row, last_column):
        self.on_deletion = True
        diff_row = (first_row - last_row) // 2
        diff_column = (first_column - last_column) // 2
        wanted_row = first_row -  diff_row
        wanted_column = first_column - diff_column
        self.buttons[wanted_row][wanted_column].config(text='')
        self.game_table[wanted_row][wanted_column] = None

        if not self.player_turn:
            self.player_one_remaining -=1
            self.player_one_pieces.pop(self.player_one_pieces.index([wanted_row, wanted_column])) 
            self.label_player_one_cards.config(text=f'Peças Restantes: {self.player_one_remaining}')
            
        else:
            self.player_two_remaining -= 1
            self.player_two_pieces.pop(self.player_two_pieces.index([wanted_row, wanted_column]))
            self.label_player_two_cards.config(text=f'Peças Restantes: {self.player_two_remaining}')
        
        if self.player_one_remaining == 0 or self.player_two_remaining == 0:
            self.endGame()
    
    def changePiecePosition(self, first_row, first_col, actual_row, actual_col, clicked_label):
        # se é o jogador 1 e ele chegou na linha mais de cima, vira super peça ou
        # se é o jogador 2 e ele chegou na linha mais de baixo vira super peça
        # caso contrário, apenas move a peça sendo ela do player 1 ou do player 2.
        self.game_table[actual_row][actual_col] = PlayerOne.SUPER_PIECE if (
            self.player_turn and actual_row == 0) else PlayerTwo.SUPER_PIECE if(
                not self.player_turn and actual_row == 7
            ) else self.game_table[first_row][first_col] 
        self.game_table[first_row][first_col] = None
        
        if self.player_turn:
            self.player_one_pieces.pop(self.player_one_pieces.index([first_row, first_col]))
            self.player_one_pieces.append([actual_row, actual_col])
        else:
            self.player_two_pieces.pop(self.player_two_pieces.index([first_row, first_col]))
            self.player_two_pieces.append([actual_row, actual_col])

        self.first_click.config(text='')
        clicked_label.config(text=self.getTileText(actual_row, actual_col), 
                             fg=self.getTileForeground(actual_row, actual_col))
        self.first_click.config(bg='white')
        self.first_click = None
    
    def mapPiece(self, piece_row, piece_column):
        adjacent_houses = self.getAdjacentTiles(piece_row, piece_column)
        print(adjacent_houses)
        for adjacent in adjacent_houses:
            if self.validaCasa(adjacent):
                other_player = PlayerTwo if self.player_turn else PlayerOne
                if self.game_table[adjacent[0]][adjacent[1]] in [
                                                                    other_player.DEFAULT_PIECE, 
                                                                    other_player.SUPER_PIECE    
                                                                ]:
                    self.checkNext(piece_row, piece_column, adjacent[0], adjacent[1])

    def changePlayerTurn(self):
        self.player_turn = not self.player_turn
        self.obrigatory_movements = {}
        self.LabelTurn.config(text='1' if self.player_turn else '2')
        self.mapPiecesObrigatory(self.player_one_pieces if self.player_turn else self.player_two_pieces) 

    def mapPiecesObrigatory(self, pieces_list):
        for piece in pieces_list:
            piece_row, piece_column = piece
            adjacent_houses = self.getAdjacentTiles(piece_row, piece_column)
            for adjacent in adjacent_houses:
                if self.validaCasa(adjacent):
                    other_player = PlayerTwo if self.player_turn else PlayerOne
                    if self.game_table[adjacent[0]][adjacent[1]] in [
                                                                other_player.DEFAULT_PIECE, 
                                                                other_player.SUPER_PIECE    
                                                            ]:
                        self.checkNext(piece_row, piece_column, adjacent[0], adjacent[1])

    def validaCasa(self, casa):
        if (casa[0] < 0 or casa[0] >= len(self.game_table)) or casa[1] < 0 or casa[1] >= len(self.game_table):
            return False
        return True
    
    def checkNext(self, piece_row, piece_col, next_row, next_col):
        diff_row = piece_row - next_row
        diff_col = piece_col - next_col
        next_row = next_row - diff_row
        next_col = next_col - diff_col

        # this line verify if the next element is not out of the table
        if (next_row < 0 or next_row >= len(self.game_table)) or next_col < 0 or next_col >= len(self.game_table):
            return False
        
        # this line verify if the next house of the direction is empty or fullfiled
        if self.game_table[next_row][next_col] is not None:
            return False
        self.addObrigatoryMovementOption(piece_row, piece_col, next_row, next_col)
        return True
    
    def addObrigatoryMovementOption(self, key_row, key_column, value_row, value_column):
        if (key_row, key_column) not in self.obrigatory_movements.keys():
            # creating the options of movements when is 
            self.obrigatory_movements[key_row, key_column] = []
        self.obrigatory_movements[key_row, key_column].append([value_row, value_column])
        
    def getTileColor(self, row, column):
        return (EVEN_TILES if (is_odd(row) and not is_odd(column)) 
                    or not is_odd(row) and is_odd(column) else ODD_TILES )

    def getTileForeground(self, row, column):
        return (
            PLAYER_ONE_COLOR if 
                self.game_table[row][column] in [PlayerOne.DEFAULT_PIECE, PlayerOne.SUPER_PIECE]
            else 
                PLAYER_TWO_COLOR if self.game_table[row][column] in [PlayerTwo.DEFAULT_PIECE, PlayerTwo.SUPER_PIECE]
                else
                    None
                )
    
    def getTileText(self, row, column):
        return (
            '⛃' if self.game_table[row][column] in [PlayerOne.DEFAULT_PIECE, PlayerTwo.DEFAULT_PIECE]
                else '♚' if self.game_table[row][column] in [PlayerOne.SUPER_PIECE, PlayerTwo.SUPER_PIECE]
                    else ''
            )
    
    def endGame(self):
        topLevelWinner = Toplevel(self.root)
        topLevelWinner.grab_set()
        topLevelWinner.resizable(False, False)
        topLevelWinner.protocol("WM_DELETE_WINDOW", self.close)
        Label(topLevelWinner,
                    text=f'Vitória do jogador {1 if self.player_one_remaining > self.player_two_remaining else 2}', 
                    font='Helvetica 14 bold').grid(columnspan=3)
        Button(topLevelWinner, text='Jogar Novamente', font='Helvetica 12 bold',
                    command=lambda wm=topLevelWinner: self.RestartGame(wm)).grid(sticky=NSEW)
        Button(topLevelWinner, text='Sair', font='Helvetica 12 bold',
                    command=self.close).grid(row=1, column=1, sticky=NSEW, columnspan=2)
        
    def close(self):
        self.root.destroy()

    def RestartGame(self, toplevel:Toplevel):
        toplevel.destroy()
        self.frame_header.destroy()
        self.frame_slots.destroy()
        self.startGame()
    
root = Tk()
app = Checkers(root)
root.mainloop()