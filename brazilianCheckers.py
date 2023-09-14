from tkinter import *
from tkinter import messagebox
from enum import Enum

from database.game import Game
from database.gamesCountDatabase import CompetitiveGamesNames
from database.playerDatabase import PlayerDBCommands

EVEN_TILES = 'white'  # blocos pares
ODD_TILES = 'brown'   # blocos ímpares
PLAYER_ONE_COLOR = 'red'
PLAYER_TWO_COLOR = 'black'

def is_odd(number):
    return True if number % 2 != 0 else False   

def showMat(mat):
    for i in range(8):
        for j in range(8):
            print(mat[i][j], ' ', end='')
        print()


class PlayerOne(Enum):
    DEFAULT_PIECE = 'PlayerOne'
    SUPER_PIECE = 'SuperPlayerOne'
    

class PlayerTwo(Enum):
    DEFAULT_PIECE = 'PlayerTwo'
    SUPER_PIECE = 'SuperPlayerTwo'


class BrazilianCheckers(Game):
    def __init__(self, root=Tk, controller=None, player1='Jogador 1', player2='Jogador 2') -> None:
        super(BrazilianCheckers, self).__init__(root, controller, 'Brazilian Checkers in tkinter')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.player_one = player1
        self.player_two = player2
        self.title_font = 'Helvetica 16 bold'
        self.sub_font = 'Helvetica 12'
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
        self.tiles_labels:list[Label] = [[None for i in range(8)] for j in range(8)]
        self.createHeader()
        self.createStartBoard()

    def _create_label(self, frame, text, **kwargs):
        label = Label(frame, text=text, **kwargs)
        label.grid()
        return label
    
    def _create_title_label(self, frame, text, **kwargs):
        return self._create_label(frame, text, font=self.title_font, **kwargs)
    
    def _create_subtitle_label(self, frame, text, **kwargs):
        return self._create_label(frame, text, font=self.sub_font, **kwargs)

    def _create_frame_player(self, name, available_pieces, column, **kwargs):
        frame_player = Frame(self.frame_header)
        self._create_title_label(frame_player, name)
        label_player = self._create_subtitle_label(frame_player, f'Peças Restantes: {available_pieces}')
        label_player.grid()

        frame_attrs = {"row": 0, "column": column, "sticky": NSEW}
        frame_attrs.update(kwargs)
        frame_player.grid(**frame_attrs)
        return label_player

    def createHeader(self):
        self.frame_header = Frame(self.root)

        self.label_player_one_cards = self._create_frame_player(self.player_one, self.player_one_remaining, 0, columnspan=2)
        self.label_player_two_cards = self._create_frame_player(self.player_two, self.player_two_remaining, 4)
        
        frameTurn = Frame(self.frame_header)
        self._create_title_label(frameTurn, 'Vez do jogador:')
        self.LabelTurn = self._create_subtitle_label(frameTurn, '1')
        frameTurn.grid(row=0, column=2, rowspan=2, sticky=NSEW)
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
        lbl.bind('<ButtonPress-1>', lambda event, row=row, column=column: self.controlMovement(row, column))
        lbl.grid(row=row, column=column)
        self.tiles_labels[row][column] = lbl

    def validateFirstClick(self, row, column):
        # if there is any capture to be done, only be able to select the piece that can capture something
        clicked_label: Label = self.tiles_labels[row][column]
        if len(self.obrigatory_movements) and (row, column) not in self.obrigatory_movements.keys():
            messagebox.showwarning('Captura obrigatória', 'Captura obrigatória existente.')
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
        if self.isDefaultPiece(piece_row, piece_column):
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

        if not is_for_capture:
            return upper_movements if self.player_turn else lower_movements
        return upper_movements + lower_movements

    def getSuperPieceMovements(self, piece_row, piece_column):
        movement_options = []
        adjacent_tiles = [
            [piece_row-1, piece_column-1],
            [piece_row-1, piece_column+1], 
            [piece_row+1, piece_column-1],
            [piece_row+1, piece_column+1]
        ]
        other_player = PlayerTwo if self.player_turn else PlayerOne
        actual_player = PlayerOne if self.player_turn else PlayerTwo
        for direction in adjacent_tiles:
            self.capture = False
            actual_tile = direction
            direction_row = piece_row - direction[0]
            direction_col = piece_column - direction[1]

            while self.isValidTile(actual_tile[0], actual_tile[1]):
                intern_tile = actual_tile
                if self.game_table[actual_tile[0]][actual_tile[1]] in [
                    actual_player.DEFAULT_PIECE, actual_player.SUPER_PIECE
                ]:
                    break
                if self.game_table[actual_tile[0]][actual_tile[1]] in [
                    other_player.DEFAULT_PIECE, other_player.SUPER_PIECE
                ]:
                    intern_tile = self.getNextPosition(actual_tile[0], actual_tile[1], direction_row, direction_col)
                    while self.isValidTile(intern_tile[0], intern_tile[1]):
                        if self.game_table[intern_tile[0]][intern_tile[1]] is not None:
                            self.capture = False
                            break
                        if not self.isEmptyTile(intern_tile[0], intern_tile[1]):
                            break
                        self.addObrigatoryMovementOption(piece_row, piece_column, intern_tile[0], intern_tile[1])
                        intern_tile = self.getNextPosition(intern_tile[0], intern_tile[1], direction_row, direction_col)
                if not self.isValidTile(intern_tile[0], intern_tile[1]):
                    break
                if self.game_table[intern_tile[0]][intern_tile[1]] is not None:
                    break
                self.has_valid_tiles = True
                movement_options.append(actual_tile)
                actual_tile = self.getNextPosition(actual_tile[0], actual_tile[1], direction_row, direction_col)
        return movement_options
    
    def getNextPosition(self, actual_row, actual_column, direction_row, direction_column):
        next_row = actual_row - direction_row
        next_column = actual_column - direction_column
        return [next_row, next_column]
    
    def mapPiece(self, piece_row, piece_column):
        if self.isDefaultPiece(piece_row, piece_column):
            self.mapNormalPiece(piece_row, piece_column)
        else:
            self.mapSuperPiece(piece_row, piece_column)

    def mapNormalPiece(self, piece_row, piece_column):
        adjacent_capture_tiles = self.getPossibleMovements(piece_row, piece_column, is_for_capture=True)
        adjacent_movement_tiles = self.getPossibleMovements(piece_row, piece_column)

        other_player = PlayerTwo if self.player_turn else PlayerOne
        for adjacent_tile in adjacent_capture_tiles:
            adjacent_tile_row, adjacent_tile_column = adjacent_tile
            if self.isValidTile(adjacent_tile_row, adjacent_tile_column):
                if self.game_table[adjacent_tile_row][adjacent_tile_column] in [
                                                                    other_player.DEFAULT_PIECE, 
                                                                    other_player.SUPER_PIECE    
                                                                ]:
                    if self.checkNext(piece_row, piece_column, adjacent_tile_row, adjacent_tile_column):
                        self.has_valid_tiles = True
                elif adjacent_tile in adjacent_movement_tiles and self.isEmptyTile(adjacent_tile_row, adjacent_tile_column):
                    self.has_valid_tiles = True
        return self.has_valid_tiles

    def mapSuperPiece(self, piece_row, piece_column):
        movement_options = []
        adjacent_tiles = [
            [piece_row-1, piece_column-1],
            [piece_row-1, piece_column+1], 
            [piece_row+1, piece_column-1],
            [piece_row+1, piece_column+1]
        ]
        other_player = PlayerTwo if self.player_turn else PlayerOne
        actual_player = PlayerOne if self.player_turn else PlayerTwo
        for direction in adjacent_tiles:
            self.capture = False
            actual_tile = direction
            direction_row = piece_row - direction[0]
            direction_col = piece_column - direction[1]

            while self.isValidTile(actual_tile[0], actual_tile[1]):
                intern_tile = actual_tile
                if self.game_table[actual_tile[0]][actual_tile[1]] in [
                    actual_player.DEFAULT_PIECE, actual_player.SUPER_PIECE
                ]:
                    break
                if self.game_table[actual_tile[0]][actual_tile[1]] in [
                    other_player.DEFAULT_PIECE, other_player.SUPER_PIECE
                ]:
                    intern_tile = self.getNextPosition(actual_tile[0], actual_tile[1], direction_row, direction_col)
                    while self.isValidTile(intern_tile[0], intern_tile[1]):
                        if self.game_table[intern_tile[0]][intern_tile[1]] is not None:
                            self.capture = False
                            break
                        if not self.isEmptyTile(intern_tile[0], intern_tile[1]):
                            break
                        self.addObrigatoryMovementOption(piece_row, piece_column, intern_tile[0], intern_tile[1])
                        intern_tile = self.getNextPosition(intern_tile[0], intern_tile[1], direction_row, direction_col)
                if not self.isValidTile(intern_tile[0], intern_tile[1]):
                    break
                if self.game_table[intern_tile[0]][intern_tile[1]] is not None:
                    break
                self.has_valid_tiles = True
                movement_options.append(actual_tile)
                actual_tile = self.getNextPosition(actual_tile[0], actual_tile[1], direction_row, direction_col)

    def controlMovement(self, row, column):
        # define the element to be moved, if there's no piece selected yet, 
        # then verify if it's a valid piece to be chosen.
        clicked_label: Label = self.tiles_labels[row][column]
        if not self.first_click:
            self.validateFirstClick(row, column)
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

        if self.game_table[first_click_row][first_click_col] in [PlayerOne.DEFAULT_PIECE, PlayerTwo.DEFAULT_PIECE]:
            if (
            len(self.obrigatory_movements) and 
                [row, column] not in 
                    self.obrigatory_movements[(first_click_row, first_click_col)]
            ):
                return
        
        possible_moves = self.getPossibleMovements(first_click_row, first_click_col)
        if not len(self.obrigatory_movements) and [row, column] not in possible_moves:
            return
        if len(self.obrigatory_movements):
            if[row, column] not in self.obrigatory_movements[(first_click_row, first_click_col)]:
                messagebox.showwarning('Captura obrigatória', 'Movimentação de peça inválida.')
                return
            self.normalRemovePiece(first_click_row, first_click_col, row, column) if \
                self.game_table[first_click_row][first_click_col] in [
                    PlayerOne.DEFAULT_PIECE, PlayerTwo.DEFAULT_PIECE
                ] else self.superRemovePiece(first_click_row, first_click_col, row, column)
            
            self.obrigatory_movements = {}
            self.changePiecePosition(first_click_row, first_click_col, row, column) 
            self.mapPiece(row, column)   
        else:
            self.changePiecePosition(first_click_row, first_click_col, row, column)    
        
        if not len(self.obrigatory_movements):
            self.can_change_first_click = True
            self.canTurnSuperPiece(row, column)
            self.changePlayerTurn()  
        else:
            self.can_change_first_click = False
            self.first_click = clicked_label
            clicked_label.config(bg='lime')
        
    def superRemovePiece(self, first_row, first_column, click_row, click_column):
        direction_row = (-1) if click_row < first_row else 1
        direction_col = (-1) if click_column < first_column else 1
        actual_row = click_row
        actual_column = click_column
        while self.game_table[actual_row][actual_column] is None:
            actual_row = actual_row - direction_row
            actual_column = actual_column - direction_col
        self.game_table[actual_row][actual_column] = None
        self.tiles_labels[actual_row][actual_column].config(text='')
        self.movePieceInList(actual_row, actual_column)

    def normalRemovePiece(self, first_row, first_column, last_row, last_column):
        self.on_deletion = True
        diff_row = (first_row - last_row) // 2
        diff_column = (first_column - last_column) // 2
        actual_row = first_row -  diff_row
        actual_column = first_column - diff_column
        self.tiles_labels[actual_row][actual_column].config(text='')
        self.game_table[actual_row][actual_column] = None
        self.movePieceInList(actual_row, actual_column)

    def movePieceInList(self, actual_row, actual_column):
        if not self.player_turn:
            self.player_one_remaining -=1
            self.player_one_pieces.pop(self.player_one_pieces.index([actual_row, actual_column])) 
            self.label_player_one_cards.config(text=f'Peças Restantes: {self.player_one_remaining}')
        else:
            self.player_two_remaining -= 1
            self.player_two_pieces.pop(self.player_two_pieces.index([actual_row, actual_column]))
            self.label_player_two_cards.config(text=f'Peças Restantes: {self.player_two_remaining}')
        if self.player_one_remaining == 0 or self.player_two_remaining == 0:
            self.finished = True
            self.root.update()
            self.endGame()

    def canTurnSuperPiece(self, row, column):
        if (self.player_turn and row == 0) or (not self.player_turn and row == 7):
            self.game_table[row][column] = (PlayerOne.SUPER_PIECE if (self.player_turn)
                else PlayerTwo.SUPER_PIECE)
            self.tiles_labels[row][column].config(text=self.getTileText(row, column))
    
    def changePiecePosition(self, first_row, first_col, actual_row, actual_column):
        # if it's player 1 and he stops in the upper row, this piece turns into super_piece else
        # if it's player 2 and he stops in the lower row, this piece turns into super_piece else
        # it just moves the piece
        clicked_label:Label = self.tiles_labels[actual_row][actual_column]
        self.changeTilesText(actual_row, actual_column, first_row, first_col)
        
        if self.player_turn:
            self.player_one_pieces.pop(self.player_one_pieces.index([first_row, first_col]))
            self.player_one_pieces.append([actual_row, actual_column])
        else:
            self.player_two_pieces.pop(self.player_two_pieces.index([first_row, first_col]))
            self.player_two_pieces.append([actual_row, actual_column])

        self.first_click.config(text='')
        clicked_label.config(text=self.getTileText(actual_row, actual_column), 
                             fg=self.getTileForeground(actual_row, actual_column))
        self.first_click.config(bg='white')
        self.first_click = None

    def changeTilesText(self, new_row, new_column, first_row, first_col):
        self.game_table[new_row][new_column] = self.game_table[first_row][first_col] 
        self.game_table[first_row][first_col] = None

    def changePlayerTurn(self):
        self.player_turn = not self.player_turn
        self.obrigatory_movements = {}
        self.LabelTurn.config(text=self.player_one if self.player_turn else self.player_two)
        self.has_valid_tiles = False
        self.mapPiecesObrigatory(self.player_one_pieces if self.player_turn else self.player_two_pieces) 
        if not self.has_valid_tiles and not self.finished:
            self.root.update()
            self.endGame()

    def mapPiecesObrigatory(self, pieces_list):
        for piece in pieces_list:
            piece_row, piece_column = piece
            self.mapPiece(piece_row, piece_column)

    def isValidTile(self, row, column):
        if (
            row < 0 
            or row >= len(self.game_table) 
            or column < 0 
            or column >= len(self.game_table)
        ):
            return False
        return True
    
    def isEmptyTile(self, row, column):
        if self.game_table[row][column] is None:
            return True
        return False
    
    def isDefaultPiece(self, piece_row, piece_column):
        return True if self.game_table[piece_row][piece_column] in [
                    PlayerOne.DEFAULT_PIECE, PlayerTwo.DEFAULT_PIECE
                ] else False

    def checkNext(self, piece_row, piece_col, next_row, next_col):
        diff_row = piece_row - next_row
        diff_col = piece_col - next_col
        next_row = next_row - diff_row
        next_col = next_col - diff_col

        # this line verify if the next element is not out of the table
        if not self.isValidTile(next_row, next_col):
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
        if self.player_one_remaining > 0 and self.player_two_remaining > 0:
            winner_player = self.player_one if not self.player_turn else self.player_two
            loser_player = self.player_two if not self.player_turn else self.player_one
            textEnd =  f'{loser_player} morreu no porco.'
            title = 'Morte no porco!!!'
        else:
            winner_player = self.player_one if self.player_turn else self.player_two
            loser_player = self.player_one if not self.player_turn else self.player_two
            textEnd =  f'{loser_player} ficou sem peças.'
            title = 'Fim de jogo!!!'

        PlayerDBCommands.setGamePlayed(CompetitiveGamesNames.BrazilianCheckers, winner_player, won=True)
        PlayerDBCommands.setGamePlayed(CompetitiveGamesNames.BrazilianCheckers, loser_player)
        textVictory = f'Vitória de: {winner_player}'
        topLevelWinner = Toplevel(self.root)
        topLevelWinner.resizable(False, False)
        topLevelWinner.protocol("WM_DELETE_WINDOW", self.close)
        topLevelWinner.title(title)
        Label(topLevelWinner,
                    text=textVictory, 
                    font='Helvetica 14 bold').grid(columnspan=3)
        Label(topLevelWinner,
                    text=textEnd, 
                    font='Helvetica 14 bold').grid(columnspan=3)
        Button(topLevelWinner, text='Jogar Novamente', font='Helvetica 12 bold',
                    command=lambda wm=topLevelWinner: self.RestartGame(wm)).grid(sticky=NSEW)
        Button(topLevelWinner, text='Sair', font='Helvetica 12 bold',
                    command=self.close).grid(row=2, column=1, sticky=NSEW, columnspan=2)
        topLevelWinner.grab_set()

    def RestartGame(self, toplevel:Toplevel):
        toplevel.destroy()
        self.frame_header.destroy()
        self.frame_slots.destroy()
        self.startGame()
    
if __name__ == '__main__':
    root = Tk()
    app = BrazilianCheckers(root)
    root.mainloop()