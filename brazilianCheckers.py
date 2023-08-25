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
        self.finished = False
        self.tiles_labels = [[None for i in range(8)] for j in range(8)]
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
                        font='None 24 bold',
                        )
        lbl.bind('<ButtonPress-1>', lambda event, lbl=lbl, row=row, column=column: self.controlMovement(lbl, row, column))
        lbl.grid(row=row, column=column)
        self.tiles_labels[row][column] = lbl

    def validateFirstClick(self, row, column, clicked_label: Label):
    # if there is any capture to be done, only be able to select the piece that can capture something
        if len(self.obrigatory_movements) and (row, column) not in self.obrigatory_movements.keys():
            return
        
        player_pieces = PlayerOne if self.player_turn else PlayerTwo
        # if the clicked tile dont have a piece of the current player, then return
        if self.game_table[row][column] not in [
                    player_pieces.DEFAULT_PIECE, 
                    player_pieces.SUPER_PIECE
                ]:
            return
        clicked_label.config(bg='lime')
        self.first_click = clicked_label
        return    

    def getPossibleMovements(self, piece_row, piece_column, is_for_capture=False):
        if self.game_table[piece_row][piece_column] in [
                PlayerOne.DEFAULT_PIECE, PlayerTwo.DEFAULT_PIECE
        ]:
            possible_movements = self.getDefaultPieceMovements(piece_row, piece_column, is_for_capture)
        else:
            possible_movements = self.getSuperPieceMovements(piece_row, piece_column)
        return possible_movements
    
    def getDefaultPieceMovements(self, piece_row, piece_column, is_for_capture=False):
        upper_movements = [
            [piece_row-1, piece_column-1],
            [piece_row-1, piece_column+1], 
        ]

        lower_movements = [
            [piece_row+1, piece_column-1],
            [piece_row+1, piece_column+1]
        ]

        if self.game_table[piece_row][piece_column] in [
                    PlayerOne.DEFAULT_PIECE, PlayerTwo.DEFAULT_PIECE
                ] and not is_for_capture:
            return upper_movements if self.player_turn else lower_movements
        return upper_movements + lower_movements

    def getSuperPieceMovements(self, piece_row, piece_column):
        return [
            [piece_row-1, piece_column-1],
            [piece_row-1, piece_column+1], 
            [piece_row+1, piece_column-1],
            [piece_row+1, piece_column+1]
        ]

    def controlMovement(self, clicked_label:Label, row, column):
        # define the element to be moved, if there's no piece selected yet, 
        # then verify if it's a valid piece to be chosen.
        if not self.first_click:
            self.validateFirstClick(row, column, clicked_label)
            return
        
        # if it isn't the first click, and is the same label of the first click, undo the click
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
        
        possible_moves = self.getPossibleMovements(first_click_row, first_click_col)
        if not len(self.obrigatory_movements) and [row, column] not in possible_moves:
            return
        if len(self.obrigatory_movements):
            if[row, column] not in self.obrigatory_movements[(first_click_row, first_click_col)]:
                return
            self.removePiece(first_click_row, first_click_col, row, column)
            self.obrigatory_movements = {}
            self.changePiecePosition(first_click_row, first_click_col, row, column, clicked_label) 
            self.mapPiece(row, column)   
        else:
            self.changePiecePosition(first_click_row, first_click_col, row, column, clicked_label)    

        if not len(self.obrigatory_movements):
            self.can_change_first_click = True
            self.canTurnSuperPiece(row, column)
            self.changePlayerTurn()  
        else:
            self.can_change_first_click = False
            self.first_click = clicked_label
            clicked_label.config(bg='lime')

    def removePiece(self, first_row, first_column, last_row, last_column):
        self.on_deletion = True
        diff_row = (first_row - last_row) // 2
        diff_column = (first_column - last_column) // 2
        wanted_row = first_row -  diff_row
        wanted_column = first_column - diff_column
        self.tiles_labels[wanted_row][wanted_column].config(text='')
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
            self.finished = True
            self.endGame()
        
    def canTurnSuperPiece(self, row, column):
        if (self.player_turn and row == 0) or (not self.player_turn and row == 7):
            self.game_table[row][column] = (PlayerOne.SUPER_PIECE if (self.player_turn)
                else PlayerTwo.SUPER_PIECE)
            self.tiles_labels[row][column].config(text=self.getTileText(row, column))
            
    
    def changePiecePosition(self, first_row, first_col, actual_row, actual_col, clicked_label):
        # if it's player 1 and he got into upper row, this piece turns into super_piece else
        # if it's player 2 and he got into lower row, this piece turns into super_piece else
        # it just moves the piece
        self.changeTilesText(actual_row, actual_col, first_row, first_col)
        
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

    def changeTilesText(self, new_row, new_column, first_row, first_col):
        self.game_table[new_row][new_column] = self.game_table[first_row][first_col] 
        self.game_table[first_row][first_col] = None

    
    def mapPiece(self, piece_row, piece_column):
        adjacent_capture_tiles = self.getPossibleMovements(piece_row, piece_column, is_for_capture=True)
        adjacent_movement_tiles = self.getPossibleMovements(piece_row, piece_column)

        other_player = PlayerTwo if self.player_turn else PlayerOne
        for adjacent_tile in adjacent_capture_tiles:
            adjacent_tile_row, adjacent_tile_column = adjacent_tile
            if self.isValidTile(adjacent_tile):
                if self.game_table[adjacent_tile_row][adjacent_tile_column] in [
                                                                    other_player.DEFAULT_PIECE, 
                                                                    other_player.SUPER_PIECE    
                                                                ]:
                    if self.checkNext(piece_row, piece_column, adjacent_tile_row, adjacent_tile_column):
                        self.has_valid_tiles = True
                elif adjacent_tile in adjacent_movement_tiles and self.isEmptyTile(adjacent_tile_row, adjacent_tile_column):
                    self.has_valid_tiles = True
        return self.has_valid_tiles

    def changePlayerTurn(self):
        self.player_turn = not self.player_turn
        self.obrigatory_movements = {}
        self.LabelTurn.config(text='1' if self.player_turn else '2')
        self.has_valid_tiles = False
        self.mapPiecesObrigatory(self.player_one_pieces if self.player_turn else self.player_two_pieces) 
        if not self.has_valid_tiles and not self.finished:
            self.noValidTiles()

    def mapPiecesObrigatory(self, pieces_list):
        for piece in pieces_list:
            piece_row, piece_column = piece
            self.mapPiece(piece_row, piece_column)
            

    def isValidTile(self, casa):
        if ((casa[0] < 0 or casa[0] >= len(self.game_table)) or casa[1] < 0 or casa[1] >= len(self.game_table)):
            return False
        return True
    
    def isEmptyTile(self, row, column):
        if self.game_table[row][column] is None:
            return True
        return False

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
        topLevelWinner.title('Fim de jogo!!!')
        topLevelWinner.protocol("WM_DELETE_WINDOW", self.close)
        Label(topLevelWinner,
                    text=f'Vitória do jogador {1 if self.player_one_remaining > self.player_two_remaining else 2}', 
                    font='Helvetica 14 bold').grid(columnspan=3)
        Button(topLevelWinner, text='Jogar Novamente', font='Helvetica 12 bold',
                    command=lambda wm=topLevelWinner: self.RestartGame(wm)).grid(sticky=NSEW)
        Button(topLevelWinner, text='Sair', font='Helvetica 12 bold',
                    command=self.close).grid(row=1, column=1, sticky=NSEW, columnspan=2)
    
    def noValidTiles(self):
        topLevelWinner = Toplevel(self.root)
        topLevelWinner.grab_set()
        topLevelWinner.resizable(False, False)
        topLevelWinner.protocol("WM_DELETE_WINDOW", self.close)
        topLevelWinner.title('Morte no porco!!!')
        Label(topLevelWinner,
                    text=f'Vitória do jogador {1 if not self.player_turn else 2}', 
                    font='Helvetica 14 bold').grid(columnspan=3)
        Label(topLevelWinner,
                    text=f'Jogador {2 if not self.player_turn else 1} morreu no porco.', 
                    font='Helvetica 14 bold').grid(columnspan=3)
        Button(topLevelWinner, text='Jogar Novamente', font='Helvetica 12 bold',
                    command=lambda wm=topLevelWinner: self.RestartGame(wm)).grid(sticky=NSEW)
        Button(topLevelWinner, text='Sair', font='Helvetica 12 bold',
                    command=self.close).grid(row=2, column=1, sticky=NSEW, columnspan=2)
        
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