from tkinter import *
from tkinter import messagebox
import random
import time

from database.game import Game
from database.gamesCountDatabase import CompetitiveGamesNames
from database.playerDatabase import PlayerDBCommands
from database.gameHistory import GamesHistoryCommands

GAME_ROWS = 5
GAME_COLUMNS = 6
PLAYER_ONE_COLOR = 'lime'
PLAYER_TWO_COLOR = 'RED'
def showMat(mat):
    for i in range(GAME_ROWS):
        for j in range(GAME_COLUMNS):
            print(mat[i][j], ' ', end='')
        print()

class TileMatching(Game):
    def __init__(self, root:Tk, controller=None, player1='Jogador 1', player2='Jogador 2'):
        super(TileMatching, self).__init__(root, controller, 'Tile Matching in tkinter')
        self.player_one = player1
        self.player_two = player2
        self.emoji_list = [
            '💀', '👽', '👾', '🤖', '🎃', 
            '😺', '🎱', '🤑', '🤠', '😈', 
            '👹', '👺', '🤡', '💩', '👻', 
        ]
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.startGame()
    
    def _slots(self, positions=False):
        if positions:
            return [[row, column] for column in range(GAME_COLUMNS) for row in range(GAME_ROWS)]
        # return [[None for column in range(GAME_COLUMNS)] for row in range(GAME_ROWS)]
        return [[None] * GAME_COLUMNS for row in range(GAME_ROWS)]
    
    def startGame(self):
        '''
        we are playing with 15 emojis as the items, 
        so the window game will have 5 rows and 6 
        columns what means it will have 30 slots.
        '''
        self.slots = self._slots()
        self.choice_one, self.choice_two = None, None
        self.button_one:None | Button = None
        self.button_two:None | Button = None
        self.player_turn = True # True para jogador 1 ou False para jogador 2, definindo o jogador da vez
        self.player_one_cards = []
        self.player_two_cards = []
        self.discovered_cards = 0
        self.fillSlots()
        self.createHeader()
        self.createButtons()

    def fillSlots(self):
        '''
        cria as opções de slots vazios (posições da tabela de acordo com seu tamanho)
        e as preenche de acordo com os emojis da lista de emoji, definindo posições aleatórias
        para os pares de emoji. (itens do jogo da memória)
        '''
        free_slots = self._slots(positions=True)
        for item in self.emoji_list:
            slot1, slot2 = random.sample(free_slots, k=2)
            free_slots.pop(free_slots.index(slot1))
            free_slots.pop(free_slots.index(slot2))
            self.slots[slot1[0]][slot1[1]] = item
            self.slots[slot2[0]][slot2[1]] = item

        # showMat(self.slots)

    def createHeader(self):
        self.frame_header = Frame(self.root)
        title_font = 'Helvetica 18 bold'
        sub_font = 'Helvetica 14'

        frame_player_one = Frame(self.frame_header)
        Label(frame_player_one, 
                 text=self.player_one, 
                 font=title_font, 
                 fg=PLAYER_ONE_COLOR
        ).grid()
        self.label_player_one_cards = Label(
            frame_player_one, 
            text=f'Cartas: {len(self.player_one_cards)}', 
            font=sub_font,
            fg=PLAYER_ONE_COLOR
        )
        self.label_player_one_cards.grid()
        
        frame_turn = Frame(self.frame_header)
        Label(frame_turn, 
                 text='Vez do jogador:', 
                 font=title_font
        ).grid()
        self.label_turn = Label(
            frame_turn, 
            text=self.player_one if self.player_turn else self.player_two, 
            font=sub_font
        )
        self.label_turn.grid()

        frame_player_two = Frame(self.frame_header)
        Label(
            frame_player_two, 
            text=self.player_two, 
            font=title_font, 
            fg=PLAYER_TWO_COLOR
        ).grid()
        self.label_player_two_cards = Label(
            frame_player_two, 
            text=f'Cartas: {len(self.player_two_cards)}', 
            font=sub_font,
            fg=PLAYER_TWO_COLOR
        )
        self.label_player_two_cards.grid()

        frame_player_one.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=NSEW)
        frame_turn.grid(row=0, column=2, rowspan=2, sticky=NSEW)
        frame_player_two.grid(row=0, column=4, rowspan=2, sticky=NSEW)
        self.frame_header.grid_columnconfigure(1, weight=1)
        self.frame_header.grid_columnconfigure(3, weight=1)
    
        self.frame_header.grid(sticky=NSEW)

    def createButtons(self):
        '''
        cria os botões clicáveis com a função de mudar o texto
        '''
        self.frame_buttons = Frame(self.root)
        for row in range(GAME_ROWS):
            for column in range(GAME_COLUMNS):
                btn = Button(self.frame_buttons, text='', 
                        width=5, height=2, relief='solid', font='None 28 bold', 
                        # command=lambda position=(row, column):self.control(position))
                )
                btn.config(command= 
                            lambda 
                                button=btn,
                                position=(row, column)
                                    :
                                    self.control(button, position))
                btn.grid(row=row, column=column, sticky=NSEW, padx=1, pady=1)
        self.frame_buttons.grid()

    def control(self, button, position):
        # verifica e valida se é o primeiro card aberto ou o segundo
        if not self.choice_one:
            self.button_one = button
            self.click1(button, position)
        elif not self.choice_two and button != self.button_one:
            self.button_two = button
            self.click2(button, position)
            self.root.update()
            time.sleep(0.6)
            self.validate()

    def click1(self, button:Button, position):
        row, column = position
        self.choice_one = self.slots[row][column]
        button.config(text=self.choice_one)

    def click2(self, button:Button, position):
        row, column = position
        self.choice_two = self.slots[row][column]
        button.config(text=self.choice_two)   

    def validate(self):
        if self.choice_one == self.choice_two:
            self.discovered_cards += 1
            self.button_one.config(state='disabled')
            self.button_one.config(bg=PLAYER_ONE_COLOR if self.player_turn else PLAYER_TWO_COLOR)
            self.button_two.config(state='disabled')
            self.button_two.config(bg=PLAYER_ONE_COLOR if self.player_turn else PLAYER_TWO_COLOR)
            
            (
                self.player_one_cards.append(self.choice_one) if self.player_turn 
                else self.player_two_cards.append(self.choice_one)
            )
            self.label_player_one_cards.config(text=f'Cartas: {len(self.player_one_cards)}')
            self.label_player_two_cards.config(text=f'Cartas: {len(self.player_two_cards)}')
            self.choice_one, self.choice_two = None, None
            self.button_one, self.button_two = None, None
            if self.discovered_cards == len(self.emoji_list):
                messagebox.showinfo('ACABOU', 'FIM DE JOGO.')
                self.endGame()
        else:
            # messagebox.showinfo('Troca de jogadores', 'Cartas não iguais, troca de jogadores.')
            self.player_turn = not self.player_turn
            self.label_turn.config(text=self.player_one if self.player_turn else self.player_two)
            self.button_one.config(text='')
            self.button_two.config(text='')
            self.choice_one, self.choice_two = None, None

    def endGame(self):
        top_level_winner = Toplevel(self.root)
        top_level_winner.grab_set()
        top_level_winner.resizable(False, False)
        top_level_winner.protocol("WM_DELETE_WINDOW", self.close)
        winner_player = self.player_one if len(self.player_one_cards) > len(self.player_two_cards) else self.player_two
        loser_player = self.player_two if len(self.player_one_cards) > len(self.player_two_cards) else self.player_one
        PlayerDBCommands.setGamePlayed(CompetitiveGamesNames.TileMatching, winner_player, won=True)
        PlayerDBCommands.setGamePlayed(CompetitiveGamesNames.TileMatching, loser_player)
        player_one_id = PlayerDBCommands.getIDByNick(self.player_one)
        player_two_id = PlayerDBCommands.getIDByNick(self.player_two)
        winner_player_id = PlayerDBCommands.getIDByNick(winner_player)
        game_name = self.getGameName()
        GamesHistoryCommands.insertNewMatch(game_name, player_one_id, player_two_id, winner_player_id)
        Label(top_level_winner,
                    text=f'Vitória de: {winner_player}', 
                    font='Helvetica 14 bold').grid(columnspan=3)
        Button(top_level_winner, text='Jogar Novamente', font='Helvetica 12 bold',
                    command=lambda wm=top_level_winner: self.restartGame(wm)).grid(sticky=NSEW)
        Button(top_level_winner, text='Sair', font='Helvetica 12 bold',
                    command=self.close).grid(row=1, column=1, sticky=NSEW, columnspan=2)

    def restartGame(self, toplevel:Toplevel):
        toplevel.destroy()
        self.frame_buttons.destroy()
        self.frame_header.destroy()
        self.startGame()

if __name__ == '__main__':
    root = Tk()
    app = TileMatching(root)
    root.mainloop()
