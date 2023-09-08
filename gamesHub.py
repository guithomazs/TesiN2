from tkinter import *
from tkinter import ttk
from classicCheckers import ClassicCheckers
from brazilianCheckers import BrazilianCheckers
from minas import Minas
from ticTacToe import TicTacToe
from tileMatching import TileMatching
from playerListScreen import Players
from leaderboards import Leaderboards
from database.playerDatabase import PlayerDBCommands
from utils import (MainTitleBar,
                   InGameTitleBar,
                   GridMainTitleBar,
                   GridInGameTitleBar,
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

        GamesHubScreen.createMenu(self.root)
        self.createCharChoice()
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

    def createCharChoice(self):
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
        players_name = []
        for item in items:
            players_name.append(item[0])
        return players_name

    def createFrameButtons(self):
        frame_buttons = LabelFrame(self.root, text='Jogos', font=LABEL_FRAME_FONT)
        GameSelectButton(frame_buttons, text='Jogo da velha',    
                        command=lambda: self.changeCurrentScreen(TicTacToe, self.root)        ).grid(sticky=NSEW, padx=2, pady=2)
        GameSelectButton(frame_buttons, text='Campo Minado',     
                        command=lambda: self.changeCurrentScreen(Minas, self.root)            ).grid(sticky=NSEW, padx=2, pady=2)
        GameSelectButton(frame_buttons, text='Jogo da Memória',  
                        command=lambda: self.changeCurrentScreen(TileMatching, self.root)     ).grid(sticky=NSEW, padx=2, pady=2)
        GameSelectButton(frame_buttons, text='Damas Clássica',   
                        command=lambda: self.changeCurrentScreen(ClassicCheckers, self.root)  ).grid(sticky=NSEW, padx=2, pady=2)
        GameSelectButton(frame_buttons, text='Damas Brasileira', 
                        command=lambda: self.changeCurrentScreen(BrazilianCheckers, self.root)).grid(sticky=NSEW, padx=2, pady=2)
        frame_buttons.grid(sticky=NSEW)
        frame_buttons.grid_columnconfigure(0, weight=1)

    @staticmethod
    def changeCurrentScreen(Screen, root):
        GamesHubScreen.cleanUp(root)
        Screen(root, controller=GamesHubScreen)

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