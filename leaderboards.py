from tkinter import *
from utils import GameSelectButton
from brazilianCheckers import BrazilianCheckers
from classicCheckers import ClassicCheckers
from mineSweeper import MineSweeper
from ticTacToe import TicTacToe
from tileMatching import TileMatching
from gameLeaderBoard import GameLeaderBoard

LABEL_FRAME_FONT = 'Arial 24 bold'
class Leaderboards:
    def __init__(self, master: Tk, controller=None) -> None:
        self.root = master
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.title('Leaderboard')
        if controller != None:
            self.controller = controller
        else:
            from gamesHub import GamesHubScreen
            self.controller = GamesHubScreen
        self.controller.createMenu(self.root)

        
        self.createFrameButtons()
        
    def createFrameButtons(self):
        frame_buttons = LabelFrame(self.root, text='Leaderboards', font=LABEL_FRAME_FONT)
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
                                 game=game 
                                 : 
                                 self.changeCurrentScreen(game, self.root)
            ).grid(sticky=NSEW, padx=2, pady=2)
        
        frame_buttons.grid(sticky=NSEW)
        frame_buttons.grid_columnconfigure(0, weight=1)

    def changeCurrentScreen(self, game, root):
        self.controller.cleanUp(root)
        self.changeCloseButtonFunction()
        GameLeaderBoard(root, game)

    def goingBack(self):
        self.controller.cleanUp(self.root)
        self.controller.rebindCloseButton(self.root)
        Leaderboards(self.root)

    def changeCloseButtonFunction(self):
        self.root.protocol('WM_DELETE_WINDOW', self.goingBack)

if __name__ == '__main__':
    app = Tk()
    tela = Leaderboards(app)
    app.mainloop()