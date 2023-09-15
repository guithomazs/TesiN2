from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from classicCheckers import ClassicCheckers
from brazilianCheckers import BrazilianCheckers
from mineSweeper import MineSweeper
from ticTacToe import TicTacToe
from tileMatching import TileMatching
from playerListScreen import Players
from leaderboards import Leaderboards
from database.playerDatabase import PlayerDBCommands
from database.gamesCountDatabase import (
    TimedGamesNames, 
    CompetitiveGamesNames
)
from utils import (
    GameSelectButton,
    PseudoMenuButton,
    WifiButton
)


LABEL_FRAME_FONT = 'Arial 24 bold'
PLAYERS_TITLE_FONT = 'Helvetica 16 bold'
PLAYERS_OPTIONS_FONT = 'Helvetica 13 bold'
class GamesHubScreen:
    def __init__(self, master: Tk) -> None:
        self.root = master
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.title('Games Hub')

        self.createMenu(self.root)
        self.createPlayerChoice()
        self.createFrameButtons()
        
    @staticmethod
    def createMenu(root:Tk):
        pseudo_menu = Frame(root)
        PseudoMenuButton(pseudo_menu, text='🏠',
                         command=lambda: GamesHubScreen.goingBack(root)).grid(row=0, column=0, sticky=NSEW)
        WifiButton(pseudo_menu, text='WIFI',
                                                                       ).grid(row=1, column=0, sticky=NSEW)
        PseudoMenuButton(pseudo_menu, text='Jogadores',
                         command=lambda: GamesHubScreen.changeCurrentScreen(Players, root)).grid(row=0, column=1, rowspan=2, sticky=NSEW)
        PseudoMenuButton(pseudo_menu, text='Leaderboards',
                         command=lambda: GamesHubScreen.changeCurrentScreen(Leaderboards, root)).grid(row=0, column=2, rowspan=2, sticky=NSEW)
        pseudo_menu.grid_columnconfigure(0, weight=1)
        pseudo_menu.grid_columnconfigure(1, weight=2)
        pseudo_menu.grid_columnconfigure(2, weight=2)
        pseudo_menu.grid(sticky=NSEW)

    def controlPlayerUnique(self, which_combobox):
        if self.p2_choice.get() != self.p1_choice.get():
            return
        self.p2_choice.set('') if which_combobox == 1 else self.p1_choice.set('')

    def createPlayerChoice(self):
        frame_players = Frame(self.root)
        players_name = self.getPlayersName()

        p1 = Label(frame_players, text='Jogador 1', font=PLAYERS_TITLE_FONT)
        self.p1_choice = ttk.Combobox(frame_players, state='readonly', values=players_name, font=PLAYERS_OPTIONS_FONT)

        p2 = Label(frame_players, text='Jogador 2', font=PLAYERS_TITLE_FONT)
        self.p2_choice = ttk.Combobox(frame_players, state='readonly', values=players_name, font=PLAYERS_OPTIONS_FONT)
        p1.grid(row=0, column=0, sticky=W, padx=15)
        p2.grid(row=0, column=1, sticky=E, padx=15)
        self.p1_choice.grid(row=1, column=0, sticky=W, padx=15)
        self.p2_choice.grid(row=1, column=1, sticky=E, padx=15)
        frame_players.grid(columnspan=2, sticky=NSEW)

        self.p1_choice.bind("<<ComboboxSelected>>", lambda event: self.controlPlayerUnique(1))
        self.p2_choice.bind("<<ComboboxSelected>>", lambda event: self.controlPlayerUnique(2))

        frame_players.grid_columnconfigure(0, weight=1)
        frame_players.grid_columnconfigure(1, weight=1)

    def getPlayersName(self):
        items = PlayerDBCommands.getDataBasePlayers()
        players_name = ['']
        for item in items:
            players_name.append(item[1])
        return players_name

    def createFrameButtons(self):
        frame_buttons = LabelFrame(self.root, text='Jogos', font=LABEL_FRAME_FONT)
        games = {
            TicTacToe: 'Jogo da velha',
            MineSweeper: 'Campo Minado',
            TileMatching: 'Jogo da Memória',
            ClassicCheckers: 'Damas Clássica',
            BrazilianCheckers: 'Damas Brasileira',
                 }
        for game, text in games.items():
            GameSelectButton(frame_buttons, text=text,    
                            command=lambda 
                                game=game,
                                player1=self.p1_choice.get(),
                                player2=self.p2_choice.get()
                                : 
                                self.canChangeScreen(
                                    game,         
                                    self.root, 
                                    player1=self.p1_choice.get(), 
                                    player2=self.p2_choice.get()
                                )
            ).grid(sticky=NSEW, padx=2, pady=2)
        
        frame_buttons.grid(sticky=NSEW)
        frame_buttons.grid_columnconfigure(0, weight=1)

    def canChangeScreen(self, Screen, root, **kwargs):
        if Screen.__name__ in CompetitiveGamesNames._member_names_:
            if not self.p1_choice.get() or not self.p2_choice.get():
                messagebox.showinfo("Aviso.", "Necessário que ambos os jogadores tenham sido selecionados")
                return
        
        if not self.p1_choice.get():
            kwargs['player1'] = self.p2_choice.get()
            kwargs['player2'] = None
        if not kwargs['player1']:
            messagebox.showinfo("Aviso.", "É necessário selecionar um jogador")
            return
        if Screen.__name__ in TimedGamesNames._member_names_:
            if kwargs['player2']:
                messagebox.showinfo("Aviso.", "Para jogos de tempo limite selecione apenas um jogador")
                return
            kwargs.pop('player2')
        self.changeCurrentScreen(Screen, root, **kwargs)

    @staticmethod
    def changeCurrentScreen(Screen, root, **kwargs):
        GamesHubScreen.cleanUp(root)
        Screen(root, controller=GamesHubScreen, **kwargs)

    @staticmethod
    def goingBack(Screen):
        GamesHubScreen.cleanUp(Screen)
        GamesHubScreen.rebindCloseButton(Screen)
        GamesHubScreen(Screen)

    @staticmethod
    def cleanUp(Screen):
        # destroy all widgets from frame
        for widget in Screen.winfo_children():
            widget.destroy()

    @staticmethod
    def rebindCloseButton(Screen):
        Screen.protocol('WM_DELETE_WINDOW', Screen.destroy)

if __name__ == '__main__':
    root = Tk()
    app = GamesHubScreen(root)
    root.mainloop()