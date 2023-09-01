from tkinter import *
from tkinter import ttk
from classicCheckers import ClassicCheckers
from brazilianCheckers import BrazilianCheckers
from minas import Minas
from velha import TicTacToe
from tileMatching import TileMatching
from playerListScreen import Players
from leaderboards import Leaderboards
from utils import (MainTitleBar,
                   InGameTitleBar,
                   GridMainTitleBar,
                   GridInGameTitleBar,
                   GameSelectButton,
                   PseudoMenuButton,
                   WifiButton
)

LABEL_FRAME_FONT = 'Arial 24 bold'
class GamesHubScreen:
    def __init__(self, master: Tk) -> None:
        self.root = master
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.title('Games Hub')

        GamesHubScreen.createMenu(self.root)
        self.createFrameButtons()
        
    @staticmethod
    def createMenu(root):
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